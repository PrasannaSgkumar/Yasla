from django.db import models

import uuid
from django.db import models
from django.contrib.auth.hashers import make_password

from django.conf import settings

class Salon(models.Model):
    class SalonCategoryChoices(models.TextChoices):
        MEN = 'Men', 'Men'
        WOMEN = 'Women', 'Women'
        UNISEX = 'Unisex', 'Unisex'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    def __str__(self):
        return self.salon_name


class SalonBranch(models.Model):
    class SalonCategoryChoices(models.TextChoices):
        MEN = 'Men', 'Men'
        WOMEN = 'Women', 'Women'
        UNISEX = 'Unisex', 'Unisex'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    def __str__(self):
        return f"{self.branch_name} ({self.city})"


class SalonGallery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Media_ID
    salon = models.ForeignKey('Salon', on_delete=models.CASCADE, related_name='gallery')
    branch = models.ForeignKey('SalonBranch', on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery')  # Optional: allows None for global salon images
    image = models.ImageField(upload_to='salon_gallery/')  # Uploads to MEDIA_ROOT/salon_gallery/

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='users')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    
    # 👇 Using choices here
    user_role = models.CharField(
        max_length=50,
        choices=UserRole.choices,
        default=UserRole.STYLIST
    )

    profile_image = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Active')  # You can also use choices here if needed
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    branches = models.ManyToManyField(SalonBranch, related_name='users')

    def __str__(self):
        return f"{self.full_name} - {self.user_role}"
    
    def save(self, *args, **kwargs):
    # Hash the password only if it’s not already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)



class Customer(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    full_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)  
    phone = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)  
    gender = models.CharField(max_length=20, choices=GenderChoices.choices, null=True, blank=True)
    profile_image = models.TextField(null=True, blank=True) 
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
    # Hash the password only if it’s not already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)





from decimal import Decimal

class Service(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        UNISEX = 'Unisex', 'Unisex'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Service_ID
    salon = models.ForeignKey('Salon', on_delete=models.CASCADE, related_name='services')
    branch = models.ForeignKey('SalonBranch', on_delete=models.SET_NULL, null=True, blank=True, related_name='services')

    service_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  # Optional: you can also use choices
    description = models.TextField()

    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Optional
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    estimated_time_min = models.PositiveIntegerField()
    gender_specific = models.CharField(
        max_length=50,
        choices=GenderChoices.choices,
        default=GenderChoices.UNISEX
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name




class Appointment(models.Model):
    class BookingStatusChoices(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        CONFIRMED = 'Confirmed', 'Confirmed'
        COMPLETED = 'Completed', 'Completed'
        CANCELLED = 'Cancelled', 'Cancelled'

    class BookingTypeChoices(models.TextChoices):
        ONLINE = 'Online', 'Online'
        OFFLINE = 'Offline', 'Offline'

    class PaymentStatusChoices(models.TextChoices):
        PAID = 'Paid', 'Paid'
        UNPAID = 'Unpaid', 'Unpaid'
        PARTIALLY_PAID = 'Partially Paid', 'Partially Paid'

    class PaymentModeChoices(models.TextChoices):
        UPI = 'UPI', 'UPI'
        CARD = 'Card', 'Card'
        WALLET = 'Wallet', 'Wallet'
        CASH = 'Cash at Salon', 'Cash at Salon'

    class BookingSourceChoices(models.TextChoices):
        APP = 'App', 'App'
        WALKIN = 'Walk-in', 'Walk-in'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  

    salon = models.ForeignKey('Salon', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    branch = models.ForeignKey('SalonBranch', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    stylist = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_stylist')

    booking_date = models.DateField(null=True, blank=True)
    time_slot = models.CharField(max_length=20, null=True, blank=True)

    status = models.CharField(
        max_length=50,
        choices=BookingStatusChoices.choices,
        default=BookingStatusChoices.PENDING,
        null=True,
        blank=True
    )
    booking_type = models.CharField(
        max_length=20,
        choices=BookingTypeChoices.choices,
        null=True,
        blank=True
    )
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatusChoices.choices,
        null=True,
        blank=True
    )
    payment_mode = models.CharField(
        max_length=50,
        choices=PaymentModeChoices.choices,
        null=True,
        blank=True
    )
    invoice_id = models.CharField(max_length=100, null=True, blank=True)

    booking_source = models.CharField(
        max_length=50,
        choices=BookingSourceChoices.choices,
        null=True,
        blank=True
    )

    assigned_by = models.CharField(max_length=255, null=True, blank=True)
    customer_message = models.TextField(null=True, blank=True)
    staff_notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    cancellation_reason = models.TextField(null=True, blank=True)
    cancelled_by = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Appointment - {self.id}"









class AppointmentService(models.Model):
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='appointment_services')
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Store final price
    duration_min = models.PositiveIntegerField(null=True, blank=True)  # Optional: override estimated time

    def __str__(self):
        return f"{self.service.service_name} for {self.appointment.id}"
    



class Payment(models.Model):
    class PaymentModeChoices(models.TextChoices):
        UPI = 'UPI', 'UPI'
        CARD = 'Card', 'Card'
        CASH = 'Cash', 'Cash'
        WALLET = 'Wallet', 'Wallet'

    class PaymentStatusChoices(models.TextChoices):
        PAID = 'Paid', 'Paid'
        FAILED = 'Failed', 'Failed'
        REFUNDED = 'Refunded', 'Refunded'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Payment_ID

    booking = models.ForeignKey('Appointment', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    payment_mode = models.CharField(
        max_length=50,
        choices=PaymentModeChoices.choices,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=50,
        choices=PaymentStatusChoices.choices,
        null=True,
        blank=True
    )

    transaction_date = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.status} - {self.amount}"




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
