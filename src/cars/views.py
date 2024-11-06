from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from .models import Car, Client, Employee,User
from .permissions import IsAdmin, IsEmployee, IsClient
from .serializers import CarSerializer, UserSerializer, ClientSerializer


# Récupérer les détails d'une voiture par son immatriculation
class CarDetailAPIView(APIView):

    permission_classes = [IsAdmin]  # Only admin can view details

    def get(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        serializer = CarSerializer(car)
        return Response(serializer.data)



class CarListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only Admin can create cars
            return [IsAdmin()]
        return [IsAdmin()]  # Allow admin to see the list of cars


class CarUpdateAPIView(APIView):
    permission_classes = [IsEmployee]  # Only employee can update the status

    def put(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            car.status = serializer.validated_data.get('status', car.status)
            car.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDeleteAPIView(APIView):
    permission_classes = [IsAdmin]  # Only admin can view details
    def delete(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarClientDetailAPIView(APIView):
    permission_classes = [IsClient]

    def get(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        if car.registration_number == request.user.car_registration_number:
            serializer = CarSerializer(car)
            return Response(serializer.data)
        return Response({"detail": "You do not have permission to view this car."}, status=status.HTTP_403_FORBIDDEN)


class RegisterEmployeeView(APIView):
    permission_classes = [IsAdmin]  # Only admin can access this view

    def post(self, request, *args, **kwargs):
        data = request.data
        data['role'] = 'employee'  # Set role to employee
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Employee added successfully."}, status=201)
        return Response(serializer.errors, status=400)

class RegisterClientView(APIView):
    permission_classes = [IsEmployee]  # Employees or logged-in users can access this view

    def post(self, request, *args, **kwargs):
        # Only allow employees to add clients
        if request.user.role != 'employee':
            return Response({"message": "You are not authorized to add clients."}, status=403)

        data = request.data
        data['role'] = 'client'  # Set role to client
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Client registered successfully."}, status=201)
        return Response(serializer.errors, status=400)
# User Login View
class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # JWT setup
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'token': token, 'role': user.role})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
