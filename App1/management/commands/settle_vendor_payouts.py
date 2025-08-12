import uuid
import math
import logging
from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.utils.timezone import make_aware, get_default_timezone

import requests
from requests.auth import HTTPBasicAuth

from App1.models import Salon, BankDetails, Vendor_Payment  # adjust import

log = logging.getLogger(__name__)

API_BASE = "https://api.razorpay.com/v1/payouts"

def _previous_week_range(today: date):
    # Find the Monday of the current week (Mon=0)
    monday_this_week = today - timedelta(days=today.weekday())
    # Previous week Mon..Sun
    week_start = monday_this_week - timedelta(days=7)
    week_end = week_start + timedelta(days=6)
    return week_start, week_end

def _week_number(week_start: date):
    # Your own definition; ISO week also OK
    return int(week_start.strftime("%Y%W"))

def _paise(amount_decimal):
    # Convert Decimal('123.45') -> 12345 (int paise)
    return int(round(float(amount_decimal) * 100))

class Command(BaseCommand):
    help = "Settle previous week's (Mon–Sun) vendor payouts on Wednesday."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Run regardless of weekday (for manual backfills/tests).",
        )
        parser.add_argument(
            "--date",
            type=str,
            help="Pretend 'today' is this date (YYYY-MM-DD) for dry runs/backfills.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Compute and log but do not hit RazorpayX.",
        )

    def handle(self, *args, **opts):
        print("Running")
        tz = get_default_timezone()
        today = date.fromisoformat(opts["date"]) if opts.get("date") else date.today()
        is_wednesday = today.weekday() == 2  # 0=Mon ... 2=Wed

        print(f"Today's date: {today}, is_wednesday: {is_wednesday}")

        if not (is_wednesday or opts["force"]):
            self.stdout.write(self.style.WARNING("Not Wednesday. Use --force to run anyway."))
            return

        week_start, week_end = _previous_week_range(today)
        week_no = _week_number(week_start)

        self.stdout.write(self.style.NOTICE(
            f"Settling payouts for week {week_no}: {week_start} to {week_end} (inclusive)"
        ))

        # Pull unpaid vendor payments in the previous week
        payments = (
            Vendor_Payment.objects
            .select_related("salon")
            .filter(
                payout_done=False,
                week_start_date=week_start,
                week_end_date=week_end,
            )
        )

        print(f"Found {payments.count()} payments to process.")

        if not payments.exists():
            self.stdout.write(self.style.WARNING("No unpaid records for that week."))
            return

        # Aggregate per salon
        by_salon = {}
        for vp in payments:
            by_salon.setdefault(vp.salon_id, {"salon": vp.salon, "total": 0, "rows": []})
            by_salon[vp.salon_id]["total"] += float(vp.amount or 0)
            by_salon[vp.salon_id]["rows"].append(vp)

        print(f"Aggregated {len(by_salon)} salons for payouts.")

        key_id = settings.RAZORPAYX_KEY_ID
        key_secret = settings.RAZORPAYX_KEY_SECRET
        account_number = settings.RAZORPAYX_ACCOUNT_NUMBER
        mode = getattr(settings, "RAZORPAYX_PAYOUT_MODE", "IMPS")

        if not all([key_id, key_secret, account_number]):
            raise RuntimeError("Missing RazorpayX credentials or account number in settings.")

        successes, failures = 0, 0

        for salon_id, bundle in by_salon.items():
            salon = bundle["salon"]
            total_amount = bundle["total"]

            print(f"Processing salon: {salon.salon_name}, total amount: {total_amount}")

            # Skip zero or negative totals
            if total_amount <= 0:
                log.warning("Salon %s total <= 0, skipping.", salon_id)
                continue

            # Fetch bank details
            try:
                bank = salon.bank_details
            except BankDetails.DoesNotExist:
                log.error("No BankDetails for salon id=%s, skipping.", salon_id)
                failures += 1
                continue

            if not bank.razorpay_fund_account_id:
                log.error("No fund_account_id for salon id=%s, skipping.", salon_id)
                failures += 1
                continue

            amount_paise = int(round(total_amount * 100))
            reference_id = f"salon-{salon_id}-wk-{week_no}"
            idempotency_key = f"{salon_id}-{week_start.isoformat()}-{week_end.isoformat()}"

            payload = {
                "account_number": account_number,
                "fund_account_id": bank.razorpay_fund_account_id,
                "amount": amount_paise,
                "currency": "INR",
                "mode": mode,  # IMPS/NEFT/RTGS
                "purpose": "payout",
                "queue_if_low_balance": True,
                "reference_id": reference_id,
                "narration": f"Weekly settlement {week_start}–{week_end}",
                "notes": {
                    "salon": salon.salon_name,
                    "week_start": str(week_start),
                    "week_end": str(week_end),
                },
            }

            self.stdout.write(f"Creating payout: salon={salon.salon_name} total={total_amount} ({amount_paise} paise)")

            if opts["dry_run"]:
                self.stdout.write(self.style.SUCCESS(f"[DRY RUN] Would create payout with idempotency={idempotency_key}"))
                continue

            try:
                resp = requests.post(
                    API_BASE,
                    json=payload,
                    headers={"X-Payout-Idempotency": idempotency_key},
                    auth=HTTPBasicAuth(key_id, key_secret),
                    timeout=30,
                )
                data = resp.json()

                if resp.status_code in (200, 201):
                    payout_id = data.get("id")
                    payout_status = data.get("status")  # queued, processing, processed, reversed etc.
                    with transaction.atomic():
                        # Mark all rows for this salon+week as paid (created/queued)
                        for row in bundle["rows"]:
                            row.transaction_id = payout_id
                            row.payout_done = True  # you can switch to a tri-state if you want webhook confirmation
                            row.save(update_fields=["transaction_id", "payout_done", "updated_at"])
                    self.stdout.write(self.style.SUCCESS(
                        f"Payout created id={payout_id} status={payout_status} for salon={salon.salon_name}"
                    ))
                    successes += 1
                else:
                    failures += 1
                    self.stderr.write(self.style.ERROR(
                        f"Payout failed for salon={salon.salon_name}: {resp.status_code} {data}"
                    ))
            except Exception as ex:
                failures += 1
                log.exception("Error creating payout for salon %s", salon_id)
                self.stderr.write(self.style.ERROR(str(ex)))

        self.stdout.write(self.style.SUCCESS(f"Done. Success={successes}, Failures={failures}"))
