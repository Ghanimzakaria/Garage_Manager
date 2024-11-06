from rest_framework import serializers
from .models import Car, User, Client, Employee


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['registration_number', 'brand', 'model', 'status']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'surname']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'surname']