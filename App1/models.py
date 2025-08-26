from django.db import models

from django.db import models
from django.contrib.auth.hashers import make_password

from django.conf import settings
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
import random
import string

from django.core.validators import RegexValidator


class Roles(models.Model):
    role_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ use auto_now, not auto_now_add for updates

    def __str__(self):
        return self.role_name

class RolePermissions(models.Model):  

    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='permissions')

    dashboard_v = models.BooleanField(default=False)

    roles_v = models.BooleanField(default=False)
    roles_a = models.BooleanField(default=False)
    roles_e = models.BooleanField(default=False)
    roles_d = models.BooleanField(default=False)
    
    users_v = models.BooleanField(default=False)
    users_a = models.BooleanField(default=False)
    users_e = models.BooleanField(default=False)
    users_d = models.BooleanField(default=False)

    vendors_v = models.BooleanField(default=False)
    vendors_a = models.BooleanField(default=False)
    vendors_e = models.BooleanField(default=False)
    vendors_d = models.BooleanField(default=False)

    branches_v = models.BooleanField(default=False)
    branches_a = models.BooleanField(default=False)
    branches_e = models.BooleanField(default=False)
    branches_d = models.BooleanField(default=False)

    staff_v = models.BooleanField(default=False)
    staff_a = models.BooleanField(default=False)
    staff_e = models.BooleanField(default=False)
    staff_d = models.BooleanField(default=False)

    clients_v = models.BooleanField(default=False)
    clients_a = models.BooleanField(default=False)
    clients_e = models.BooleanField(default=False)
    clients_d = models.BooleanField(default=False)

    category_v = models.BooleanField(default=False)
    category_a = models.BooleanField(default=False)
    category_e = models.BooleanField(default=False)
    category_d = models.BooleanField(default=False)

    services_v = models.BooleanField(default=False)
    services_a = models.BooleanField(default=False)
    services_e = models.BooleanField(default=False)
    services_d = models.BooleanField(default=False)
    
    schedule_v = models.BooleanField(default=False)
    schedule_a = models.BooleanField(default=False)
    schedule_e = models.BooleanField(default=False)
    schedule_d = models.BooleanField(default=False)

    bookings_v = models.BooleanField(default=False)
    bookings_a = models.BooleanField(default=False)
    bookings_e = models.BooleanField(default=False)
    bookings_d = models.BooleanField(default=False)

    payment_v = models.BooleanField(default=False)
    payment_a = models.BooleanField(default=False)
    payment_e = models.BooleanField(default=False)
    payment_d = models.BooleanField(default=False)

    def __str__(self):
        return f"Permissions for {self.role.role_name}"

class Admin_User(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, related_name='admin_users') 

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)




class Salon(models.Model):
    class SalonCategoryChoices(models.TextChoices):
        MEN = 'Men', 'Men'
        WOMEN = 'Women', 'Women'
        UNISEX = 'Unisex', 'Unisex'
    class SalonStatusChoices(models.TextChoices):
        ONLINE = 'Online', 'Online'
        OFFLINE = 'Offline', 'Offline'

    salon_name = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.TextField(null=True, blank=True)  # Can store URL or path
    vendor_type = models.CharField(max_length=100)
    salon_category = models.CharField(
        max_length=100,
        choices=SalonCategoryChoices.choices,
        default=SalonCategoryChoices.UNISEX
    )
    business_registration = models.CharField(max_length=100, null=True, blank=True)
    gstin = models.CharField(max_length=15, null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    salon_status = models.CharField(
        max_length=10,
        choices=SalonStatusChoices.choices,
        default=SalonStatusChoices.OFFLINE  
    )

    def __str__(self):
        return self.salon_name

class BankDetails(models.Model):
    salon = models.OneToOneField('Salon', on_delete=models.CASCADE, related_name='bank_details')
    account_holder_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^[A-Z]{4}0[A-Z0-9]{6}$', 'Enter a valid IFSC code')]
    )
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_contact_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_fund_account_id = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.salon.salon_name} - {self.account_holder_name}"



class SalonBranch(models.Model):
    class SalonCategoryChoices(models.TextChoices):
        MEN = 'Men', 'Men'
        WOMEN = 'Women', 'Women'
        UNISEX = 'Unisex', 'Unisex'

    class SalonStatusChoices(models.TextChoices):
        ONLINE = 'Online', 'Online'
        OFFLINE = 'Offline', 'Offline'

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='branches')
    salon_category = models.CharField(
        max_length=100,
        choices=SalonCategoryChoices.choices,
        default=SalonCategoryChoices.UNISEX
    )
    branch_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    working_days = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    salon_status = models.CharField(
        max_length=10,
        choices=SalonStatusChoices.choices,
        default=SalonStatusChoices.OFFLINE  # Default is now Offline
    )

    def __str__(self):
        return f"{self.branch_name} ({self.city})"


class SalonGallery(models.Model):  # Media_ID
    salon = models.ForeignKey('Salon', on_delete=models.CASCADE, related_name='gallery')
    branch = models.ForeignKey('SalonBranch', on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery')  # Optional: allows None for global salon images
    image = models.ImageField(upload_to='salon_gallery/') 

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        branch_info = f" - {self.branch.branch_name}" if self.branch else ""
        return f"{self.salon.salon_name}{branch_info}"



class User(models.Model):
    class UserRole(models.TextChoices):
        ADMIN = 'Admin', 'Admin'
        SUB_ADMIN = 'Sub Admin', 'Sub Admin'
        STYLIST = 'Stylist', 'Stylist'
        RECEPTIONIST = 'Receptionist', 'Receptionist'
        MANAGER = 'Manager', 'Manager'

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='users')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    user_role = models.CharField(
        max_length=50,
        choices=UserRole.choices,
        default=UserRole.STYLIST
    )

    profile_image = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Active')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    branches = models.ManyToManyField(SalonBranch, related_name='users', blank=True)
    fcm_token=models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - {self.user_role}"
    
    def save(self, *args, **kwargs):
   
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



class Customer(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'
  
    full_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)  
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)  
    gender = models.CharField(max_length=20, choices=GenderChoices.choices, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True) 
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    fcm_token=models.TextField(null=True, blank=True)
    fav_salons = models.ManyToManyField(Salon, null=True, blank=True)

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
    # Hash the password only if it’s not already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Service_Category(models.Model):
    service_category_name = models.CharField(max_length=255,null=True, blank=True, unique=True)
    service_category_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.service_category_name





class Service(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        UNISEX = 'Unisex', 'Unisex'
  # Service_ID
   
    service_name = models.CharField(max_length=255)
    category = models.ForeignKey(Service_Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    popular=models.BooleanField(default=False)
    gender_specific = models.CharField(
        max_length=50,
        choices=GenderChoices.choices,
        default=GenderChoices.UNISEX
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name




from datetime import timedelta
from django.db import models, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError


class Appointment(models.Model):
    # Foreign Keys
    salon   = models.ForeignKey('Salon', on_delete=models.SET_NULL, null=True, blank=True)
    branch  = models.ForeignKey('SalonBranch', on_delete=models.SET_NULL, null=True, blank=True)
    stylist = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)

    # Appointment Timing
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime   = models.DateTimeField(null=True, blank=True)
    duration=models.DurationField(null=True, blank=True)


    # Status & Payment Info
    class BookingStatusChoices(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        CONFIRMED = 'Confirmed', 'Confirmed'
        COMPLETED = 'Completed', 'Completed'
        CANCELLED = 'Cancelled', 'Cancelled'
        Accepted=  'Accepted', 'Accepted'
        Declined=  'Declined', 'Declined'

    status = models.CharField(max_length=20, choices=BookingStatusChoices.choices,
                              default=BookingStatusChoices.PENDING)

    class PaymentStatusChoices(models.TextChoices):
        PAID = 'Paid', 'Paid'
        UNPAID = 'Unpaid', 'Unpaid'
        PARTIALLY_PAID = 'Partially Paid', 'Partially Paid'

    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices,
                                      blank=True, null=True)

    class PaymentModeChoices(models.TextChoices):
        UPI = 'UPI', 'UPI'
        CARD = 'Card', 'Card'
        WALLET = 'Wallet', 'Wallet'
        CASH = 'Cash at Salon', 'Cash at Salon'

    payment_mode = models.CharField(max_length=20, choices=PaymentModeChoices.choices,
                                    blank=True, null=True)

    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    customer_message = models.TextField(blank=True, null=True)
    staff_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True )
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    payment_verified = models.BooleanField(default=False)
    payment_time = models.DateTimeField(blank=True, null=True)
    refund_status = models.CharField(max_length=50, blank=True, null=True)
    otp_code=models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.id
    




    def __str__(self):
        return f"Appointment #{self.id} with {self.stylist}"

class AppointmentService(models.Model):
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='appointment_services')
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Store final price
    duration_min = models.PositiveIntegerField(null=True, blank=True)  # Optional: override estimated time

    def __str__(self):
        return f"{self.service.service_name} for {self.appointment.id}"



class SalonServiceAvailability(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='available_in')

    # Optional link to salon or branch (only one should be filled)
    salon = models.ForeignKey('Salon', on_delete=models.CASCADE, null=True, blank=True, related_name='services_available')
    branch = models.ForeignKey('SalonBranch', on_delete=models.CASCADE, null=True, blank=True, related_name='services_available')
    description=models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_avaiable=models.BooleanField(default=False, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    completion_time = models.DurationField(help_text="Time format: hh:mm:ss (e.g., 00:45:00)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(salon__isnull=False, branch__isnull=True) |
                    models.Q(salon__isnull=True, branch__isnull=False)
                ),
                name="only_one_location",  
            ),
            models.UniqueConstraint(
                fields=['service', 'salon'],
                condition=models.Q(salon__isnull=False),
                name='unique_service_per_salon'
            ),
            models.UniqueConstraint(
                fields=['service', 'branch'],
                condition=models.Q(branch__isnull=False),
                name='unique_service_per_branch'
            ),
        ]

    def __str__(self):
        location = self.branch.branch_name if self.branch else self.salon.salon_name
        return f"{self.service.service_name} @ {location}"


class Feedback(models.Model):
   
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    SUB_RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    feedback_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='feedbacks')
    booking = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='feedbacks')
    stylist = models.ForeignKey('User', on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_text = models.TextField(blank=True, null=True)
    cleanliness = models.IntegerField(choices=SUB_RATING_CHOICES, blank=True, null=True)
    punctuality = models.IntegerField(choices=SUB_RATING_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.feedback_id} by {self.customer.username}"

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
        indexes = [
            models.Index(fields=['customer', 'booking']),
        ]





class Salon_Service_Category(models.Model):
    service_category_name = models.CharField(max_length=255,null=True, blank=True, unique=True)
    service_category_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_salon=models.ForeignKey(Salon, on_delete=models.CASCADE, null=True, blank=True)
    created_branch=models.ForeignKey(SalonBranch, on_delete=models.CASCADE, null=True, blank=True)
    approved=models.BooleanField(default=False)
    approved_by=models.CharField(max_length=25, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.service_category_name
    


class Salon_Service(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        UNISEX = 'Unisex', 'Unisex'
        
    service_name = models.CharField(max_length=255)
    category = models.ForeignKey(Salon_Service_Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    gender_specific = models.CharField(
        max_length=50,
        choices=GenderChoices.choices,
        default=GenderChoices.UNISEX
    )
    created_salon=models.ForeignKey(Salon, on_delete=models.CASCADE, null=True, blank=True)
    created_branch=models.ForeignKey(SalonBranch, on_delete=models.CASCADE, null=True, blank=True)
    approved=models.BooleanField(default=False)
    approved_by=models.CharField(max_length=25, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name
    

class PasswordResetCode(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=10)  

    def __str__(self):
        return f"{self.customer.email} - {self.code}"
    

class PasswordResetCodeForUser(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=10)  

    def __str__(self):
        return f"{self.user.email} - {self.code}"
    

class Vendor_Payment(models.Model):
    salon=models.ForeignKey(Salon, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    payment_date=models.DateTimeField(auto_now_add=True)
    week_no=models.IntegerField(null=True, blank=True)
    week_start_date=models.DateField(null=True, blank=True)
    week_end_date=models.DateField(null=True, blank=True)
    transaction_id=models.CharField(max_length=255, null=True, blank=True)
    payout_done=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.salon.salon_name} - {self.amount}"
    
    