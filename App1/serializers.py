from rest_framework import serializers
from .models import *

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField(write_only=True)

class CustomerLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField()
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


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentService
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
