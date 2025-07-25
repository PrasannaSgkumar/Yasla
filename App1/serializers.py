from rest_framework import serializers
from .models import *

class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField() 
    password = serializers.CharField(write_only=True)

class CustomerLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'


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
    class Meta:
        model = AppointmentService
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    appointment_services = AppointmentServiceSerializer(many=True, read_only=True)
    class Meta:
        model = Appointment
        fields = '__all__'



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['id', 'last_login', 'created_at', 'updated_at']
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

    class Meta:
        model = SalonServiceAvailability
        fields = [
            'id', 'service', 'service_name', 'salon_id', 'branch_id',
            'salon', 'branch', 'is_available', 'cost',
            'completion_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'salon', 'branch', 'service_name']

    def validate(self, data):
        salon = data.get('salon_id')
        branch = data.get('branch_id')

        if not salon and not branch:
            raise serializers.ValidationError("Either 'salon_id' or 'branch_id' must be provided.")
        if salon and branch:
            raise serializers.ValidationError("Provide only one: either 'salon_id' or 'branch_id', not both.")

        return data

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