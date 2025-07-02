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

    #login Api's
    path('customer_login', CustomerLoginView.as_view(), name='customer-login'),
    path('user_login', UserLoginView.as_view(), name='user-login'),


    #Super Admin Urls
    #Super Admin Urls
   
    path('register/vendor/', RegisterVendorAPIView.as_view(), name='register_vendor'),
    path('service-categories/', ServiceCategoryListView.as_view(), name='service_category_list'),
    path('api/services/', ServiceListView.as_view(), name='service_list'),
  
     path('login', superadminlogin, name="login"),
    path('dashboard', superadmin_dashboard, name="dashboard"),
    
    path('vendors', saloontable, name="vendors"),
    path('vendor/add', add_saloon, name="add_saloon"),
    path('salon/delete/<uuid:id>/', delete_vendor, name="delete_salon"),
    path('salon/view/<uuid:id>/', view_vendor, name="view_salon"),

    path('branch/add/<uuid:id>/', add_branch, name="add_branch"),
    path('branch/edit/<uuid:id>/', edit_branch, name="edit_branch"),
    path('branch/delete/<uuid:id>/', delete_branch, name="delete_branch"),
    path('branch/view/<uuid:id>/', view_branch, name="view_branch"),

    path('user/add/<uuid:id>/', add_user, name="add_user"),
    path('user/edit/<uuid:id>/', edit_user, name="edit_user"),
    path('user/delete/<uuid:id>/', delete_user, name="delete_user"),
    path('user/view/<uuid:id>/', view_user, name="view_user"),

    path('customers/list/', customer_table, name='customer_table'),
    # path('customer/add/', add_customer, name='add_customer'),
    # path('customer/edit/<uuid:id>/', edit_customer, name='edit_customer'),
    # path('customer/delete/<uuid:id>/', delete_customer, name='delete_customer'),
    path('customer/view/<uuid:id>/', view_customer, name='view_customer'),

    path('payment/list/', payment_table, name='payment_table'),
    path('payment/view/<uuid:id>/', view_payment, name='view_payment'),

    path('service/list/', service_table, name='service_table'),  
    path('service/add/', add_service, name='add_service'),
    path('service/edit/<uuid:id>/', edit_service, name='edit_service'),
    path('service/delete/<uuid:id>/', delete_service, name='delete_service'),
    path('service/view/<uuid:id>/', view_service, name='view_service'),
    path('service/category', service_category_table, name="service_category_table"),
    path('add_category/',add_category, name='add_category'),
   
    path('edit_category/<int:id>/', edit_category, name='edit_category'),
    path('delete_category/<int:id>/', delete_category, name='delete_category'),

]