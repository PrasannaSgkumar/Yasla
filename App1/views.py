from django.shortcuts import render
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





class UserLoginView(APIView):
    @extend_schema(request=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email_or_phone = serializer.validated_data['email_or_phone']
            password = serializer.validated_data['password']
            fcm_token = request.data.get('fcm_token')

            try:
                user = User.objects.get(Q(email=email_or_phone) | Q(phone=email_or_phone))
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