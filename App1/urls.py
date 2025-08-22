from django.urls import path
from .views import *

urlpatterns = [
    path('admin-forgotpassword/', adminforgotpassword, name='adminforgotpassword'),
    path('razorpay/payment/<str:payment_id>/', get_payment_settlement_details, name='get_payment_settlement_details'),
    path('admin-send-otp/', send_otp, name='send_otp'),
    path('admin-verify-otp/', verify_otp, name='verify_otp'),
    path('admin-reset-password/', reset_password, name='reset_password'),
    path('initiate/payment/<int:appointment_id>/', PaymentInitiateAPI.as_view(), name="payment_initiate"),
    path("payment/verify/", PaymentVerifyAPI.as_view(), name="payment_verify"),
    path('salons/', SalonView.as_view(), name='salon-list-create'),
    path('salons/<int:id>/', SalonDetailView.as_view(), name='salon-detail'),
    # path('payment-verify/', PaymentVerifyView.as_view(), name='payment_verify'),
    path("payment-verify/", payment_verify, name="payment_verify"),
    # Salon Branch U
    path('salon-branches/', SalonBranchView.as_view(), name='salon-branch-list-create'),
    path('salon-branches/<int:id>/', SalonBranchDetailView.as_view(), name='salon-branch-detail'),

    path('bank-details/', BankDetailsView.as_view(), name='bank-details'),
    path('bank-details/<int:salon_id>/', BankDetailsDetailView.as_view(), name='bank-details-by-salon'),
    path('customer/forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('customer/reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('user/forgot-password/', ForgotPasswordUserAPIView.as_view(), name='user-forgot-password'),
    path('user/reset-password/', ResetPasswordUserAPIView.as_view(), name='user-reset-password'),

    # Salon Gallery URLs
    path('salon-galleries/', SalonGalleryView.as_view(), name='salon-gallery-list-create'),
    path('salon-galleries/<int:id>/', SalonGalleryDetailView.as_view(), name='salon-gallery-detail'),
    path('salons/service/<int:service_id>/', SalonsByServiceView.as_view(), name='salons-by-service'),

    # User URLs
    path('users/', UserView.as_view(), name='user-list-create'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),

    # Customer URLs
    path('customers/', CustomerView.as_view(), name='customer-list-create'),
    path('customers/<int:id>/', CustomerDetailView.as_view(), name='customer-detail'),

    # Service URLs
    path('services/', ServiceView.as_view(), name='service-list-create'),
    path('services/<int:id>/', ServiceDetailView.as_view(), name='service-detail'),

    # Appointment URLs
    path('appointments/', AppointmentView.as_view(), name='appointment-list-create'),
    path('appointments/<int:id>/', AppointmentDetailView.as_view(), name='appointment-detail'),

    # Appointment Service URLs
    path('appointment-services/', AppointmentServiceView.as_view(), name='appointment-service-list-create'),
    path('appointment-services/<int:id>/', AppointmentServiceDetailView.as_view(), name='appointment-service-detail'),

    # Payment URLs
    # path('payments/', PaymentView.as_view(), name='payment-list-create'),
    # path('payments/<int:id>/', PaymentDetailView.as_view(), name='payment-detail'),
    
    path('appointments/stylist/<int:stylist_id>/',StylistAppointmentsView.as_view(), name='stylist-appointments' ),
    path('appointments/customer/<int:customer_id>/',CustomerAppointmentsView.as_view(),name='customer-appointments'),
    
    # Feedback URLs
    path('feedbacks/', FeedbackView.as_view(), name='feedback-list-create'),
    path('feedbacks/<int:id>/', FeedbackDetailView.as_view(), name='feedback-detail'),
    path('salon/<int:salon_id>/services/<str:gender>/',SalonServicesByGenderView.as_view(),name='salon-services-by-gender' ),

    #login Api's
    path('customer_login', CustomerLoginView.as_view(), name='customer-login'),
    path('user_login', UserLoginView.as_view(), name='user-login'),
    path('api/service-availability/', SalonServiceAvailabilityListCreateAPI.as_view(), name='availability-list-create'),
    path('api/service-availability/<int:id>/', SalonServiceAvailabilityDetailAPI.as_view(), name='availability-detail'),
    path('services/filter-by-gender/', FilterServicesByGender.as_view(), name='filter_services_by_gender'),

    path('api/salon-services/', SalonServiceView.as_view(), name='salon-services'),
    path('api/salon-services/<int:id>/', SalonServiceDetailView.as_view(), name='salon-service-detail'),

    path('api/service-categories/', SalonServiceCategoryView.as_view(), name='service-category-list-create'),
    path('api/service-categories/<int:id>/', SalonServiceCategoryDetailView.as_view(), name='service-category-detail'),
    
   
    path('register/vendor/', RegisterVendorAPIView.as_view(), name='register_vendor'),
    path('service-categories/', ServiceCategoryListView.as_view(), name='service_category_list'),
    path('api/services/', ServiceListView.as_view(), name='service_list'),
  
    path('login', adminlogin, name="login"),
    path('dashboard', superadmin_dashboard, name="dashboard"),
    path('vendors/list/', salon_table, name="vendors_table"),
    path('vendor/add', add_salon, name="add_salon"),
    path('salon/edit/<int:id>/', edit_salon, name='edit_salon'),
    path('salon/delete/<int:id>/', delete_vendor, name="delete_salon"),
    path('salon/view/<int:id>/', view_vendor, name="view_salon"),

    path('branch/add/<int:id>/', add_branch, name="add_branch"),
    path('branch/edit/<int:id>/', edit_branch, name="edit_branch"),
    path('branch/delete/<int:id>/', delete_branch, name="delete_branch"),
    path('branch/view/<int:id>/', view_branch, name="view_branch"),

    path('user/add/<int:id>/', add_user, name="add_user"),
    path('user/edit/<int:id>/', edit_user, name="edit_user"),
    path('user/delete/<int:id>/', delete_user, name="delete_user"),
    path('user/view/<int:id>/', view_user, name="view_user"),

    path('customers/list/', customer_table, name='customer_table'),
    # path('customer/add/', add_customer, name='add_customer'),
    # path('customer/edit/<int:id>/', edit_customer, name='edit_customer'),
    # path('customer/delete/<int:id>/', delete_customer, name='delete_customer'),
    path('customer/view/<int:id>/', view_customer, name='view_customer'),

    path('payment/list/', payment_table, name='payment_table'),
    path('payment/view/<int:id>/', view_payment, name='view_payment'),

    path('service/list/', service_table, name='service_table'),  
    path('service/add/', add_service, name='add_service'),
    path('service/edit/<int:id>/', edit_service, name='edit_service'),
    path('service/delete/<int:id>/', delete_service, name='delete_service'),
    path('service/view/<int:id>/', view_service, name='view_service'),

    path('service/category/list/', service_category_table, name="service_category_table"),
    path('add_category/',add_category, name='add_category'),
    path('edit_category/<int:id>/', edit_category, name='edit_category'),
    path('delete_category/<int:id>/', delete_category, name='delete_category'),

    path('salon_service_category/', salon_service_category, name="salon_service_category"),
    path('salon_services_new/<int:id>/', salon_service_table, name="salon_services_new"),
    path('approve-category/<int:category_id>/service/<int:service_id>/', approve_service_category, name='approve-category'),

    path('roles/list/', roles_table, name='roles_table'),
    path('roles/add/', add_role, name='add_role'),
    path('roles/edit/<int:id>/', edit_role, name='edit_role'),
    path('roles/delete/<int:id>/', delete_role, name='delete_role'),
    path('role_permissions/<int:role_id>/', role_permissions, name='role_permissions'),

    path('admin_user/list/', admin_user_table, name='admin_user_table'),
    path('admin_user/add/', add_admin_user, name='add_admin_user'),
    path('admin_user/edit/<int:id>/', edit_admin_user, name='edit_admin_user'),
    path('admin_user/delete/<int:id>/', delete_admin_user, name='delete_admin_user'),

    path('bookings/list/', booking_table, name='booking_table'),
    path('schedule/list/', schedule_table, name='schedule_table'),
    path('booking/view/<int:id>/', view_appointment, name='view_appointment'),
    path('logout/', logout_user, name='logout'),
    path('pay/<int:appointment_id>/', payment_page, name='payment_page'),
    path('', home, name='home'),
    

]