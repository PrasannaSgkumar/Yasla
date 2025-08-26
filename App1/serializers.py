from rest_framework import serializers
from .models import *

class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField() 
    password = serializers.CharField(write_only=True)
    fcm_token = serializers.CharField(required=False, allow_blank=True)

class CustomerLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
    fcm_token = serializers.CharField(required=False, allow_blank=True)


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'


class CustomerFavSalonSerializer(serializers.ModelSerializer):
    fav_salons = SalonSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "full_name", "fav_salons"]


class SalonBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonBranch
        fields = '__all__'


class SalonGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonGallery
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        sensitive_fields = ['password']
        for field in sensitive_fields:
            rep.pop(field, None)
        return rep

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        for field in ['password']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        for key, value in validated_data.items():
            if key not in ['password']:
                setattr(instance, key, value)
        instance.save()
        return instance



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        sensitive_fields = ['password']
        for field in sensitive_fields:
            rep.pop(field, None)
        return rep

    def create(self, validated_data):
        customer = Customer(**validated_data)
        customer.save()
        return customer

    def update(self, instance, validated_data):
        for field in ['password']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        for key, value in validated_data.items():
            if key not in ['password']:
                setattr(instance, key, value)
        instance.save()
        return instance


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class AppointmentServiceSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.service_name', read_only=True)  # ✅ declare before Meta

    class Meta:
        model = AppointmentService
        fields = [
            'id', 
            'appointment', 
            'service', 
            'service_name',  # ✅ explicitly listed here
            'price', 
            'duration_min'
        ]



class AppointmentSerializer(serializers.ModelSerializer):
    appointment_services = AppointmentServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Appointment
        fields = '__all__'






class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id',  'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'salon': {'read_only': True}  # ✅ this is important!
        }


class SalonRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(write_only=True)

    class Meta:
        model = Salon
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        salon = Salon.objects.create(**validated_data)
        User.objects.create(salon=salon, **user_data)
        return salon
    
class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Category
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer()  # Nested

    class Meta:
        model = Service
        fields = '__all__'


class SalonServiceAvailabilitySerializer(serializers.ModelSerializer):
    salon_id = serializers.IntegerField(required=False, write_only=True)
    branch_id = serializers.IntegerField(required=False, write_only=True)
    salon = serializers.StringRelatedField(read_only=True)
    branch = serializers.StringRelatedField(read_only=True)
    service_name = serializers.CharField(source='service.service_name', read_only=True)
    category_name = serializers.CharField(source='service.category.service_category_name', read_only=True)
    class Meta:
        model = SalonServiceAvailability
        fields = [
            'id', 'service', 'service_name', 'salon_id', 'branch_id',
            'salon', 'branch', 'is_avaiable', 'cost', 'category_name',
            'completion_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'salon', 'branch', 'service_name']

    

    def create(self, validated_data):
        salon_id = validated_data.pop('salon_id', None)
        branch_id = validated_data.pop('branch_id', None)

        if salon_id:
            validated_data['salon'] = Salon.objects.get(id=salon_id)
        if branch_id:
            validated_data['branch'] = SalonBranch.objects.get(id=branch_id)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('salon_id', None)
        validated_data.pop('branch_id', None)
        return super().update(instance, validated_data)




class SalonServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon_Service_Category
        fields = '__all__'
        read_only_fields = ['approved', 'approved_by', 'approved_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['approved'] = False  # enforce approval False
        return super().create(validated_data)


class SalonServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon_Service
        fields = '__all__'
        read_only_fields = ['approved', 'approved_by', 'approved_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['approved'] = False  # enforce approval False
        return super().create(validated_data)
    


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = [
            'id',
            'account_holder_name',
            'bank_name',
            'account_number',
            'ifsc_code',
            'upi_id',
            'razorpay_contact_id',
            'razorpay_fund_account_id',
            'is_verified',
        ]
        read_only_fields = ['razorpay_contact_id', 'razorpay_fund_account_id', 'is_verified']




class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6)


class ForgotPasswordUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=6)