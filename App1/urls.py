from django.urls import path
from .views import *

urlpatterns = [

    # Salon URLs
    path('salons/', SalonView.as_view(), name='salon-list-create'),
    path('salons/<uuid:id>/', SalonDetailView.as_view(), name='salon-detail'),

    # Salon Branch URLs
    path('salon-branches/', SalonBranchView.as_view(), name='salon-branch-list-create'),
    path('salon-branches/<uuid:id>/', SalonBranchDetailView.as_view(), name='salon-branch-detail'),

    # Salon Gallery URLs
    path('salon-galleries/', SalonGalleryView.as_view(), name='salon-gallery-list-create'),
    path('salon-galleries/<uuid:id>/', SalonGalleryDetailView.as_view(), name='salon-gallery-detail'),

    # User URLs
    path('users/', UserView.as_view(), name='user-list-create'),
    path('users/<uuid:id>/', UserDetailView.as_view(), name='user-detail'),

    # Customer URLs
    path('customers/', CustomerView.as_view(), name='customer-list-create'),
    path('customers/<uuid:id>/', CustomerDetailView.as_view(), name='customer-detail'),

    # Service URLs
    path('services/', ServiceView.as_view(), name='service-list-create'),
    path('services/<uuid:id>/', ServiceDetailView.as_view(), name='service-detail'),

    # Appointment URLs
    path('appointments/', AppointmentView.as_view(), name='appointment-list-create'),
    path('appointments/<uuid:id>/', AppointmentDetailView.as_view(), name='appointment-detail'),

    # Appointment Service URLs
    path('appointment-services/', AppointmentServiceView.as_view(), name='appointment-service-list-create'),
    path('appointment-services/<uuid:id>/', AppointmentServiceDetailView.as_view(), name='appointment-service-detail'),

    # Payment URLs
    path('payments/', PaymentView.as_view(), name='payment-list-create'),
    path('payments/<uuid:id>/', PaymentDetailView.as_view(), name='payment-detail'),

    # Feedback URLs
    path('feedbacks/', FeedbackView.as_view(), name='feedback-list-create'),
    path('feedbacks/<int:id>/', FeedbackDetailView.as_view(), name='feedback-detail'),
    
]