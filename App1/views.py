from django.shortcuts import redirect, render
from jsonschema import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi







class UserLoginView(APIView):
    @extend_schema(request=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            fcm_token = request.data.get('fcm_token')

            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "User with the given email or phone does not exist"
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not check_password(password, user.password):
                return Response({
                    "status": "error",
                    "message": "Invalid email/phone or password"
                }, status=status.HTTP_401_UNAUTHORIZED)

            # if fcm_token:
            #     user.fcm_token = fcm_token
            #     user.save()

            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "user_id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "phone": user.phone,
                    "user_role": user.user_role,
                    "status": user.status,
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Invalid input",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class CustomerLoginView(APIView):
    @extend_schema(request=CustomerLoginSerializer)
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            password = serializer.validated_data['password']
            

            try:
                customer = Customer.objects.get(phone=phone)
            except Customer.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Customer with the given phone number does not exist"
                }, status=status.HTTP_401_UNAUTHORIZED)

            if not check_password(password, customer.password):
                return Response({
                    "status": "error",
                    "message": "Invalid phone number or password"
                }, status=status.HTTP_401_UNAUTHORIZED)

            # if fcm_token:
            #     customer.fcm_token = fcm_token
            #     customer.save()

            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "customer_id": customer.id,
                    "phone": customer.phone,
                    "full_name": customer.full_name,
                    "gender": customer.gender,
                    
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Invalid input",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class SalonView(APIView):
    def get(self, request):
        salons = Salon.objects.all()
        serializer = SalonSerializer(salons, many=True)
        return Response({
            "status": "success",
            "message": "Salons retrieved successfully",
            "data": serializer.data
        })

    @extend_schema(request=SalonSerializer)
    def post(self, request):
        serializer = SalonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Salon created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Salon creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class SalonDetailView(APIView):
    def get(self, request, id):
        try:
            salon = get_object_or_404(Salon, id=id)
            serializer = SalonSerializer(salon)
            return Response({
                "status": "success",
                "message": "Salon retrieved successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to retrieve salon",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=SalonSerializer)
    def put(self, request, id):
        try:
            salon = get_object_or_404(Salon, id=id)
            serializer = SalonSerializer(salon, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Salon updated successfully",
                    "data": serializer.data
                })
            return Response({
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to update salon",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            salon = get_object_or_404(Salon, id=id)
            salon.delete()
            return Response({
                "status": "success",
                "message": "Salon deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to delete salon",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class SalonBranchView(APIView):
    def get(self, request):
        branches = SalonBranch.objects.all()
        serializer = SalonBranchSerializer(branches, many=True)
        return Response({
            "status": "success",
            "message": "Salon Branches retrieved successfully",
            "data": serializer.data
        })

    @extend_schema(request=SalonBranchSerializer)
    def post(self, request):
        serializer = SalonBranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Salon Branch created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Salon Branch creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class SalonBranchDetailView(APIView):
    def get(self, request, id):
        try:
            branch = get_object_or_404(SalonBranch, id=id)
            serializer = SalonBranchSerializer(branch)
            return Response({
                "status": "success",
                "message": "Salon Branch retrieved successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to retrieve salon branch",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=SalonBranchSerializer)
    def put(self, request, id):
        try:
            branch = get_object_or_404(SalonBranch, id=id)
            serializer = SalonBranchSerializer(branch, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Salon Branch updated successfully",
                    "data": serializer.data
                })
            return Response({
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to update salon branch",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            branch = get_object_or_404(SalonBranch, id=id)
            branch.delete()
            return Response({
                "status": "success",
                "message": "Salon Branch deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to delete salon branch",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@method_decorator(csrf_exempt, name='dispatch')
class SalonGalleryView(APIView):
    def get(self, request):
        galleries = SalonGallery.objects.all()
        serializer = SalonGallerySerializer(galleries, many=True)
        return Response({
            "status": "success",
            "message": "Salon Galleries retrieved successfully",
            "data": serializer.data
        })

    @extend_schema(request=SalonGallerySerializer)
    def post(self, request):
        serializer = SalonGallerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Salon Gallery image uploaded successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Image upload failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class SalonGalleryDetailView(APIView):
    def get(self, request, id):
        try:
            gallery = get_object_or_404(SalonGallery, id=id)
            serializer = SalonGallerySerializer(gallery)
            return Response({
                "status": "success",
                "message": "Salon Gallery image retrieved successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to retrieve gallery image",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=SalonGallerySerializer)
    def put(self, request, id):
        try:
            gallery = get_object_or_404(SalonGallery, id=id)
            serializer = SalonGallerySerializer(gallery, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Salon Gallery image updated successfully",
                    "data": serializer.data
                })
            return Response({
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to update gallery image",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            gallery = get_object_or_404(SalonGallery, id=id)
            gallery.delete()
            return Response({
                "status": "success",
                "message": "Salon Gallery image deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to delete gallery image",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            "status": "success",
            "message": "Users retrieved successfully",
            "data": serializer.data
        })

    @extend_schema(request=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "User created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "User creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(APIView):
    def get(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserSerializer(user)
            return Response({
                "status": "success",
                "message": "User retrieved successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to retrieve user",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=UserSerializer)
    def put(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "User updated successfully",
                    "data": serializer.data
                })
            return Response({
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to update user",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            user.delete()
            return Response({
                "status": "success",
                "message": "User deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to delete user",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class CustomerView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response({
            "status": "success",
            "message": "Customers retrieved successfully",
            "data": serializer.data
        })

    @extend_schema(request=CustomerSerializer)
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Customer created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Customer creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class CustomerDetailView(APIView):
    def get(self, request, id):
        try:
            customer = get_object_or_404(Customer, id=id)
            serializer = CustomerSerializer(customer)
            return Response({
                "status": "success",
                "message": "Customer retrieved successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to retrieve customer",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=CustomerSerializer)
    def put(self, request, id):
        try:
            customer = get_object_or_404(Customer, id=id)
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "message": "Customer updated successfully",
                    "data": serializer.data
                })
            return Response({
                "status": "error",
                "message": "Invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to update customer",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            customer = get_object_or_404(Customer, id=id)
            customer.delete()
            return Response({
                "status": "success",
                "message": "Customer deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to delete customer",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@method_decorator(csrf_exempt, name='dispatch')
class ServiceView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response({
            "status": "success",
            "message": "Services retrieved successfully",
            "data": serializer.data
        })

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Service created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Service creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ServiceDetailView(APIView):
    def get(self, request, id):
        service = get_object_or_404(Service, id=id)
        serializer = ServiceSerializer(service)
        return Response({
            "status": "success",
            "message": "Service retrieved successfully",
            "data": serializer.data
        })

    def put(self, request, id):
        service = get_object_or_404(Service, id=id)
        serializer = ServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Service updated successfully",
                "data": serializer.data
            })
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        service = get_object_or_404(Service, id=id)
        service.delete()
        return Response({
            "status": "success",
            "message": "Service deleted successfully"
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class AppointmentView(APIView):
    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response({
            "status": "success",
            "message": "Appointments retrieved successfully",
            "data": serializer.data
        })

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Appointment created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Appointment creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class AppointmentDetailView(APIView):
    def get(self, request, id):
        appointment = get_object_or_404(Appointment, id=id)
        serializer = AppointmentSerializer(appointment)
        return Response({
            "status": "success",
            "message": "Appointment retrieved successfully",
            "data": serializer.data
        })

    def put(self, request, id):
        appointment = get_object_or_404(Appointment, id=id)
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Appointment updated successfully",
                "data": serializer.data
            })
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        appointment = get_object_or_404(Appointment, id=id)
        appointment.delete()
        return Response({
            "status": "success",
            "message": "Appointment deleted successfully"
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class AppointmentServiceView(APIView):
    def get(self, request):
        services = AppointmentService.objects.all()
        serializer = AppointmentServiceSerializer(services, many=True)
        return Response({
            "status": "success",
            "message": "Appointment Services retrieved successfully",
            "data": serializer.data
        })

    def post(self, request):
        serializer = AppointmentServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Appointment Service created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Appointment Service creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class AppointmentServiceDetailView(APIView):
    def get(self, request, id):
        service = get_object_or_404(AppointmentService, id=id)
        serializer = AppointmentServiceSerializer(service)
        return Response({
            "status": "success",
            "message": "Appointment Service retrieved successfully",
            "data": serializer.data
        })

    def put(self, request, id):
        service = get_object_or_404(AppointmentService, id=id)
        serializer = AppointmentServiceSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Appointment Service updated successfully",
                "data": serializer.data
            })
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        service = get_object_or_404(AppointmentService, id=id)
        service.delete()
        return Response({
            "status": "success",
            "message": "Appointment Service deleted successfully"
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentView(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response({
            "status": "success",
            "message": "Payments retrieved successfully",
            "data": serializer.data
        })

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Payment created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Payment creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentDetailView(APIView):
    def get(self, request, id):
        payment = get_object_or_404(Payment, id=id)
        serializer = PaymentSerializer(payment)
        return Response({
            "status": "success",
            "message": "Payment retrieved successfully",
            "data": serializer.data
        })

    def put(self, request, id):
        payment = get_object_or_404(Payment, id=id)
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Payment updated successfully",
                "data": serializer.data
            })
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        payment = get_object_or_404(Payment, id=id)
        payment.delete()
        return Response({
            "status": "success",
            "message": "Payment deleted successfully"
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackView(APIView):
    def get(self, request):
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response({
            "status": "success",
            "message": "Feedbacks retrieved successfully",
            "data": serializer.data
        })

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Feedback created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Feedback creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackDetailView(APIView):
    def get(self, request, id):
        feedback = get_object_or_404(Feedback, feedback_id=id)
        serializer = FeedbackSerializer(feedback)
        return Response({
            "status": "success",
            "message": "Feedback retrieved successfully",
            "data": serializer.data
        })

    def put(self, request, id):
        feedback = get_object_or_404(Feedback, feedback_id=id)
        serializer = FeedbackSerializer(feedback, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Feedback updated successfully",
                "data": serializer.data
            })
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        feedback = get_object_or_404(Feedback, feedback_id=id)
        feedback.delete()
        return Response({
            "status": "success",
            "message": "Feedback deleted successfully"
        }, status=status.HTTP_200_OK)
    

@method_decorator(csrf_exempt, name='dispatch')
class ServiceCategoryListView(APIView):

    @extend_schema(
        responses={200: ServiceCategorySerializer(many=True)},
        description="List all service categories"
    )
    def get(self, request):
        try:
            categories = Service_Category.objects.all().order_by('-created_at')
            serializer = ServiceCategorySerializer(categories, many=True)
            return Response({
                "status": "success",
                "message": "Service categories retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Failed to retrieve service categories",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ServiceListView(APIView):

    @extend_schema(
        description="List all services or filter by category_id, gender_specific, or both",
        parameters=[
            OpenApiParameter(name='category_id', type=int, description='UUID of the Service Category'),
            OpenApiParameter(name='gender_specific', type=str, description='Male / Female / Unisex')
        ],
        responses={200: ServiceSerializer(many=True)}
    )
    def get(self, request):
        category_id = request.query_params.get('category_id')
        gender = request.query_params.get('gender_specific')
        print(category_id)
        services = Service.objects.all()

        if category_id:
            services = services.filter(category=int(category_id))
        if gender:
            services = services.filter(gender_specific=gender)

        print(services)
        serializer = ServiceSerializer(services, many=True)
        return Response({
            "status": "success",
            "message": "Services retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

class SalonServiceAvailabilityListCreateAPI(APIView):

    def get(self, request):
        salon_id = request.query_params.get('salon_id')
        branch_id = request.query_params.get('branch_id')

        if not salon_id and not branch_id:
            return Response({
                'status': 'error',
                'message': 'Please provide salon_id or branch_id as a query parameter.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if salon_id:
            availabilities = SalonServiceAvailability.objects.filter(salon_id=salon_id)
        else:
            availabilities = SalonServiceAvailability.objects.filter(branch_id=branch_id)

        serializer = SalonServiceAvailabilitySerializer(availabilities, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SalonServiceAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Service availability created successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SalonServiceAvailabilityDetailAPI(APIView):

    def get(self, request, id):
        instance = get_object_or_404(SalonServiceAvailability, id=id)
        serializer = SalonServiceAvailabilitySerializer(instance)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        instance = get_object_or_404(SalonServiceAvailability, id=id)
        serializer = SalonServiceAvailabilitySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Service availability updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


#SuperAdmin Views



def superadminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Superadmin.objects.get(username=username)
            if check_password(password, user.password):
                request.session['superadmin_username'] = username
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
            else:
                print("invalid id or pass")
                messages.error(request, 'Invalid username or password')
                return render(request, 'admin/admin_login.html')
        except Superadmin.DoesNotExist:
            print("does not exist")
            messages.error(request, 'Invalid username or password')
            return render(request, 'admin/admin_login.html')

    return render(request, 'admin/admin_login.html')

def superadmin_dashboard(request):
    username = request.session.get('superadmin_username')
    if not username:
        return redirect('login')

    try:
        user = Superadmin.objects.get(username=username)
    except Superadmin.DoesNotExist:
        return redirect('login')

    context = {
        'user': user,
        'total_vendors': Salon.objects.count(),
        'total_salons': SalonBranch.objects.count(),
        'total_stylists': User.objects.filter(user_role='Stylist').count(),
        'total_clients': Customer.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_revenue': Appointment.objects.aggregate(total=models.Sum('bill_amount'))['total'] or 0
    }

    return render(request, 'admin/dashboard.html', context)
    
def saloontable(request):
    user=request.session.get('superadmin_username')
    
    if not user:
        
        return redirect('login')
    else:
        user=Superadmin.objects.get(username=user)
        saloon=Salon.objects.all()
        context={
            'user':user,
            'saloon':saloon
        }
        return render(request, 'admin/salon_table.html', context)



def add_saloon(request):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')

    if request.method == 'POST':
        salon_name = request.POST.get('salonName')
        vendor_name = request.POST.get('vendorName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        alternate_phone = request.POST.get('alternatePhone')
        vendor_type = request.POST.get('vendorType')
        salon_category = request.POST.get('salonCategory')
        business_registration = request.POST.get('businessRegistration')
        gstin = request.POST.get('gstin')
        opening_time = request.POST.get('openingTime')
        closing_time = request.POST.get('closingTime')
        street_address = request.POST.get('streetAddress')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        country = request.POST.get('country')
        latitude = request.POST.get('latitude') or None
        longitude = request.POST.get('longitude') or None
        profile_image = request.FILES.get('profileImage')

        if Salon.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'admin/salon_form.html')

        if Salon.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return render(request, 'admin/salon_form.html')

        if business_registration and Salon.objects.filter(business_registration=business_registration).exists():
            messages.error(request, "Business Registration number already exists.")
            return render(request, 'admin/salon_form.html')

        if gstin and Salon.objects.filter(gstin=gstin).exists():
            messages.error(request, "GSTIN already exists.")
            return render(request, 'admin/salon_form.html')

        Salon.objects.create(
            salon_name=salon_name,
            vendor_name=vendor_name,
            email=email,
            phone=phone,
            alternate_phone=alternate_phone,
            vendor_type=vendor_type,
            salon_category=salon_category,
            business_registration=business_registration,
            gstin=gstin,
            opening_time=opening_time,
            closing_time=closing_time,
            street_address=street_address,
            locality=locality,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
            latitude=latitude,
            longitude=longitude,
            profile_image=profile_image
        )

        messages.success(request, "Vendor added successfully.")
        return redirect('vendors')

    return render(request, 'admin/salon_form.html')


def delete_vendor(request, id):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')
    
    try:
        vendor = Salon.objects.get(id=id)
        if vendor:
            vendor.delete()
            messages.success(request, "Vendor deleted successfully.")
        else:
            messages.error(request, "Vendor not found.")
    except Salon.DoesNotExist:
        messages.error(request, "Vendor not found.")
    return redirect('vendors')


def view_vendor(request, id):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')

    try:
        vendor = Salon.objects.get(id=id)
    except Salon.DoesNotExist:
        messages.error(request, "Vendor not found.")
        return redirect('vendors')

    salon_branches = SalonBranch.objects.filter(salon_id=id)
    users = User.objects.filter(salon_id=id)

    return render(request, 'admin/salon_details.html', {
        'vendor': vendor,
        'salon_branches': salon_branches,
        'users': users,
    })




def add_branch(request, id):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')

    try:
        salon = Salon.objects.get(id=id)
    except Salon.DoesNotExist:
        messages.error(request, "Selected salon does not exist.")
        return redirect('vendors')

    if request.method == 'POST':
        branch_name = request.POST.get('branchName')
        salon_category = request.POST.get('salonCategory')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        street_address = request.POST.get('streetAddress')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        country = request.POST.get('country')
        latitude = request.POST.get('latitude') or None
        longitude = request.POST.get('longitude') or None
        opening_time = request.POST.get('openingTime') or None
        closing_time = request.POST.get('closingTime') or None
        working_days = request.POST.get('workingDays')
        is_active = request.POST.get('isActive') == 'true'

        if SalonBranch.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'admin/salon_branch_form.html', {'salon': salon})

        if SalonBranch.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return render(request, 'admin/salon_branch_form.html', {'salon': salon})

        SalonBranch.objects.create(
            salon=salon,
            branch_name=branch_name,
            salon_category=salon_category,
            email=email,
            phone=phone,
            street_address=street_address,
            locality=locality,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
            latitude=latitude,
            longitude=longitude,
            opening_time=opening_time,
            closing_time=closing_time,
            working_days=working_days,
            is_active=is_active
        )

        messages.success(request, "Branch added successfully!")
        return redirect('view_salon', id=salon.id)

    return render(request, 'admin/salon_branch_form.html', {'salon': salon})



def edit_branch(request, id):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')

    branch = get_object_or_404(SalonBranch, id=id)

    if request.method == 'POST':
        salon_id = request.POST.get('salon_name') or request.POST.get('salon_id')
        try:
            salon = Salon.objects.get(id=salon_id)
        except Salon.DoesNotExist:
            messages.error(request, "Selected salon does not exist.")
            return render(request, 'admin/salon_branch_form.html', {
                'branch': branch,
                'salon': branch.salon
            })

        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if SalonBranch.objects.filter(email=email).exclude(id=branch.id).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'admin/salon_branch_form.html', {
                'branch': branch,
                'salon': salon,
            })

        if SalonBranch.objects.filter(phone=phone).exclude(id=branch.id).exists():
            messages.error(request, "Phone number already exists.")
            return render(request, 'admin/salon_branch_form.html', {
                'branch': branch,
                'salon': salon,
            })
        
        branch.salon = salon
        branch.branch_name = request.POST.get('branchName')
        branch.salon_category = request.POST.get('salonCategory')
        branch.email = email
        branch.phone = phone
        branch.street_address = request.POST.get('streetAddress')
        branch.locality = request.POST.get('locality')
        branch.city = request.POST.get('city')
        branch.state = request.POST.get('state')
        branch.pincode = request.POST.get('pincode')
        branch.country = request.POST.get('country')
        branch.latitude = request.POST.get('latitude') or None
        branch.longitude = request.POST.get('longitude') or None
        branch.opening_time = request.POST.get('openingTime')
        branch.closing_time = request.POST.get('closingTime')
        branch.working_days = request.POST.get('workingDays')
        branch.is_active = request.POST.get('isActive') == 'true'
        branch.save()

        messages.success(request, "Branch details are updated successfully.")
        return redirect('view_salon', id=salon.id)

    return render(request, 'admin/salon_branch_form.html', {
        'branch': branch,
        'salon': branch.salon
    })


def delete_branch(request, id):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')
    
    try:
        branch = SalonBranch.objects.get(id=id)
        if branch:
            branch.delete()
            messages.success(request, "Branch deleted successfully.")
        else:
            messages.error(request, "Branch not found.")
    except SalonBranch.DoesNotExist:
        messages.error(request, "Branch not found.")

    return redirect('view_salon', id=branch.salon.id)


def view_branch(request, id):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')

    try:
        branch = SalonBranch.objects.get(id=id)
    except SalonBranch.DoesNotExist:
        messages.error(request, "Branch not found.")
        return redirect('view_salon', id=branch.salon.id)


    return render(request, 'admin/salon_branch_details.html', {
        'branch': branch,
    })

def add_user(request, id):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')

    salon = get_object_or_404(Salon, id=id)
    branches = SalonBranch.objects.filter(salon=salon)

    context={
        'salon': salon,
        'branches': branches,
    }

    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user_role = request.POST.get('userRole')
        status = request.POST.get('status')
        profile_image = request.FILES.get('profileImage')
        selected_branch_ids = request.POST.getlist('branchId')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'admin/user_form.html', context)

        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return render(request, 'admin/user_form.html', context)

        user_obj = User(
            salon=salon,
            full_name=full_name,
            email=email,
            phone=phone,
            password=password,
            user_role=user_role,
            status=status,
        )

        if profile_image:
            user_obj.profile_image = profile_image

        try:
            user_obj.save()
            user_obj.branches.set(SalonBranch.objects.filter(id__in=selected_branch_ids))
            messages.success(request, "User added successfully.")
            return redirect('view_salon', id=salon.id)
        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, 'admin/user_form.html', context)

def edit_user(request, id):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')

    edit_user = get_object_or_404(User, id=id)
    salon = edit_user.salon
    branches = SalonBranch.objects.filter(salon=salon)

    context={
        'edit_user': edit_user,
        'salon': salon,
        'branches': branches,
    }

    if request.method == 'POST':

        email = request.POST.get('email')
        phone = request.POST.get('phone')


        edit_user.full_name = request.POST.get('fullName')
        edit_user.email = email
        edit_user.phone = phone
        edit_user.user_role = request.POST.get('userRole')
        edit_user.status = request.POST.get('status')

        if request.FILES.get('profileImage'):
            edit_user.profile_image = request.FILES.get('profileImage')

        selected_branch_ids = request.POST.getlist('branchId')

        if User.objects.filter(email=email).exclude(id=edit_user.id).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'admin/user_form.html', context)

        if User.objects.filter(phone=phone).exclude(id=edit_user.id).exists():
            messages.error(request, "Phone number already exists.")
            return render(request, 'admin/user_form.html', context)

        try:
            edit_user.save()
            edit_user.branches.set(SalonBranch.objects.filter(id__in=selected_branch_ids))
            messages.success(request, "User details updated successfully.")
            return redirect('view_salon', id=salon.id)
        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, 'admin/user_form.html', context)


def delete_user(request, id):
    user = request.session.get('superadmin_username')
    if not user:
        return redirect('login')
    try:
        user = User.objects.get(id=id)
        if user:
            user.delete()
            messages.success(request, "User deleted successfully.")
        else:
            messages.error(request, "User not found.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")

    return redirect('view_salon', id=user.salon.id)


def view_user(request, id):
    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('dashboard')  # or redirect to a user list

    return render(request, 'admin/user_details.html', {
        'user': user,
    })


def customer_table(request):

    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')
    
    customers = Customer.objects.all()

    return render(request, 'admin/customer_table.html',{'customers':customers})

# def add_customer(request):

#     user_session = request.session.get('superadmin_username')
#     if not user_session:
#         return redirect('login')
    
#     if request.method == 'POST':
#         full_name = request.POST.get('fullName')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         password = request.POST.get('password')
#         gender = request.POST.get('gender')
#         address = request.POST.get('address')
#         city = request.POST.get('city')
#         pincode = request.POST.get('pincode')
#         profile_image = request.FILES.get('profileImage')


#         if Customer.objects.filter(phone=phone).exists():
#             messages.error(request, "Phone number already exists.")
#             return redirect('add_customer')
        
#         if Customer.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists.")
#             return redirect('add_customer')

#         customer = Customer(
#             full_name=full_name,
#             email=email,
#             phone=phone,
#             password=password,
#             gender=gender,
#             address=address,
#             city=city,
#             pincode=pincode
#         )

#         if profile_image:
#             customer.profile_image = profile_image

#         customer.save()
#         messages.success(request, "Customer added successfully.")
#         return redirect('customer_table')  

#     return render(request, 'admin/customer_form.html')


# def edit_customer(request, id):

#     user_session = request.session.get('superadmin_username')
#     if not user_session:
#         return redirect('login')
    
#     edit_customer = get_object_or_404(Customer, id=id)

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')

#         if Customer.objects.filter(phone=phone).exclude(id=edit_customer.id).exists():
#             messages.error(request, "Phone number already exists.")
#             return render(request, 'admin/customer_form.html', {'edit_customer':edit_customer})

#         if Customer.objects.filter(email=email).exclude(id=edit_customer.id).exists():
#             messages.error(request, "Email already exists.")
#             return render(request, 'admin/customer_form.html', {'edit_customer':edit_customer})

#         edit_customer.full_name = request.POST.get('fullName')
#         edit_customer.email = email
#         edit_customer.phone = phone
#         edit_customer.gender = request.POST.get('gender')
#         edit_customer.address = request.POST.get('address')
#         edit_customer.city = request.POST.get('city')
#         edit_customer.pincode = request.POST.get('pincode')

#         if request.FILES.get('profileImage'):
#             edit_customer.profile_image = request.FILES['profileImage']

#         edit_customer.save()
#         messages.success(request, "Customer updated successfully.")
#         return redirect('customer_table')  

#     return render(request, 'admin/customer_form.html', {
#         'edit_customer': edit_customer
#     })


# def delete_customer(request, id):

#     user_session = request.session.get('superadmin_username')
#     if not user_session:
#         return redirect('login')
    
#     customer = get_object_or_404(Customer, id=id)
#     customer.delete()
#     messages.success(request, "Customer deleted successfully.")
#     return redirect('customer_table')     

def view_customer(request, id):
    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')

    try:
        customer = Customer.objects.get(id=id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found.")
        return redirect('customer_table')

    return render(request, 'admin/customer_details.html', {
        'customer': customer,
    })

def payment_table(request):

    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')

    payments = Payment.objects.all()

    return render(request, 'admin/payment_table.html', {'payments': payments})


def service_table(request):

    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')

    services = Service.objects.all()

    return render(request, 'admin/service_table.html', {'services': services})



def view_payment(request, id):
    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')

    try:
        payment = Payment.objects.get(id=id)
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found.")
        return redirect('payment_table')

    return render(request, 'admin/payment_details.html', {
        'payment': payment,
    })
def add_service(request):
    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')

    categories = Service_Category.objects.all()

    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        gender_specific = request.POST.get('gender_specific')

        if Service.objects.filter(service_name=service_name).exists():
            messages.error(request, "Service name already exists.")
            return render(request, 'admin/service_form.html', {
                'category': categories,
                'service_name': service_name,
                'description': description,
                'gender_specific': gender_specific
            })

        # Get the category instance
        category = Service_Category.objects.filter(id=category_id).first()

        service = Service(
            service_name=service_name,
            category=category,
            description=description,
            gender_specific=gender_specific
        )
        service.save()
        messages.success(request, "Service added successfully.")
        return redirect('service_table')

    return render(request, 'admin/service_form.html', {
        'category': categories
    })


def edit_service(request, id):
    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')

    edit_service = get_object_or_404(Service, id=id)
    categories = Service_Category.objects.all()

    if request.method == 'POST':
        edit_service.service_name = request.POST.get('service_name')
        category_id = request.POST.get('category')
        edit_service.category = Service_Category.objects.filter(id=category_id).first()
        edit_service.description = request.POST.get('description')
        edit_service.gender_specific = request.POST.get('gender_specific')

        edit_service.save()
        messages.success(request, "Service updated successfully.")
        return redirect('service_table')

    return render(request, 'admin/service_form.html', {
        'edit_service': edit_service,
        'category': categories
    })


def delete_service(request, id):
    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')
    
    service = get_object_or_404(Service, id=id)
    service.delete()
    messages.success(request, "Service deleted successfully.")
    return redirect('service_table')


def view_service(request, id):
    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')

    try:
        service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        messages.error(request, "Service not found.")
        return redirect('service_table')

    return render(request, 'admin/service_details.html', {
        'service': service,
    })



class RegisterVendorAPIView(APIView):
    
    @swagger_auto_schema(
        request_body=SalonRegistrationSerializer,
        responses={201: "Vendor and User created successfully", 400: "Bad request"},
        operation_description="Register a new vendor (Salon) and an associated user."
    )
    def post(self, request):
        serializer = SalonRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vendor and user created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def service_category_table(request):
    user_session = request.session.get('superadmin_username')
    if not user_session:
        return redirect('login')
    
    categories = Service_Category.objects.all()
    return render(request, 'admin/service_category.html', {
        'categories': categories,
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Service_Category

def add_category(request):
    if request.method == 'POST':
        service_name = request.POST.get('service_name', '').strip()
        description = request.POST.get('description', '').strip()

        if not service_name:
            messages.error(request, "Service name is required.")
            return redirect('service_category_table')

        if Service_Category.objects.filter(service_category_name=service_name).exists():
            messages.error(request, "Service Category name already exists.")
            return redirect('service_category_table')

        service = Service_Category.objects.create(
            service_category_name=service_name,
            service_category_description=description
        )
        messages.success(request, "Service Category added successfully.")
        return redirect('service_category_table')  # or redirect to list view

    return render(request, 'admin/service_category_form.html')


def edit_category(request, service_id):
    service = get_object_or_404(Service_Category, id=service_id)

    if request.method == 'POST':
        service_name = request.POST.get('service_name', '').strip()
        description = request.POST.get('description', '').strip()

        if not service_name:
            messages.error(request, "Service name is required.")
            return redirect('service_category_table')

        # Check for duplicate only if name changed
        if Service_Category.objects.exclude(id=service_id).filter(service_category_name=service_name).exists():
            messages.error(request, "Another service Category with this name already exists.")
            return redirect('service_category_table')

        service.service_category_name = service_name
        service.service_category_description = description
        service.save()
        messages.success(request, "Service Category updated successfully.")
        return redirect('service_category_table')

    return render(request, 'admin/service_category_form.html', {
        'edit_service': service
    })


def delete_category(request, service_id):
    service = get_object_or_404(Service_Category, id=service_id)
    service.delete()
    messages.success(request, "Service Category deleted successfully.")
    return redirect('service_category_table')