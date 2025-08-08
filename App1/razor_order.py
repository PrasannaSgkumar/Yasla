from decimal import Decimal
from django.shortcuts import get_object_or_404
import razorpay
from django.conf import settings

from datetime import timedelta
from django.utils.timezone import make_aware
from django.db.models import Sum
import datetime
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Vendor_Payment, Appointment, BankDetails
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



def create_razorpay_contact_and_fund(bank_details):
    contact = client.contact.create({
        "name": bank_details.salon.salon_name,
        "email": bank_details.salon.email,
        "contact": bank_details.salon.phone,
        "type": "vendor",
        "reference_id": f"salon_{bank_details.salon.id}"
    })

    # Create Fund Account
    fund_account = client.fund_account.create({
        "contact_id": contact["id"],
        "account_type": "bank_account",
        "bank_account": {
            "name": bank_details.account_holder_name,
            "ifsc": bank_details.ifsc_code,
            "account_number": bank_details.account_number
        }
    })
    bank_details.razorpay_contact_id = contact["id"]
    bank_details.razorpay_fund_account_id = fund_account["id"]
    bank_details.is_verified = True
    bank_details.save()

    return {
        "contact_id": contact["id"],
        "fund_account_id": fund_account["id"]
    }






def create_order(amount_in_rupees):
    return client.order.create({
        "amount": int(float(amount_in_rupees) * 100),
        "currency": "INR",
        "payment_capture": 1
    })









def process_vendor_payment(appointment):
    start_dt = appointment.start_datetime.date()
    week_start = start_dt - timedelta(days=start_dt.weekday())  
    week_end = week_start + timedelta(days=6)  
    week_no = start_dt.isocalendar()[1]
    amount_to_add = appointment.bill_amount * Decimal('0.9')

    
    vendor_payment, created = Vendor_Payment.objects.get_or_create(
        salon=appointment.salon,
        week_no=week_no,
        week_start_date=week_start,
        week_end_date=week_end,
        payout_done=False,
        defaults={
            "amount": amount_to_add
        }
    )

    if not created:
        vendor_payment.amount += amount_to_add
        vendor_payment.save()

    return vendor_payment





class VerifyPaymentView(APIView):
    def post(self, request):
        try:
            razorpay_order_id = request.data.get("razorpay_order_id")
            razorpay_payment_id = request.data.get("razorpay_payment_id")
            razorpay_signature = request.data.get("razorpay_signature")
            payment_mode = request.data.get("payment_mode")

            appointment = get_object_or_404(Appointment, razorpay_order_id=razorpay_order_id)

            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Update appointment payment details
            appointment.razorpay_payment_id = razorpay_payment_id
            appointment.razorpay_signature = razorpay_signature
            appointment.payment_verified = True
            appointment.payment_time = now()
            appointment.payment_status = Appointment.PaymentStatusChoices.PAID
            appointment.payment_mode = payment_mode or Appointment.PaymentModeChoices.UPI
            appointment.status = Appointment.BookingStatusChoices.CONFIRMED
            appointment.save()

            # Add vendor payment record for weekly payout
            process_vendor_payment(appointment)

            return Response({"message": "Payment verified and vendor payment updated."}, status=status.HTTP_200_OK)

        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Payment verification failed."}, status=status.HTTP_400_BAD_REQUEST)


