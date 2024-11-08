from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from .models import Car,User
from .permissions import IsAdmin, IsEmployee, IsClient
from .serializers import CarSerializer, UserSerializer

# Récupérer les détails d'une voiture par son immatriculation
class CarDetailAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        serializer = CarSerializer(car)
        return Response(serializer.data)


class CarLISTAPIView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

class CarCreateAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self,request):
        data = request.data
        print("Assigned Employee:", data.get("assigned_employee"))
        print("Client:", data.get("client"))
        try:
            employee_username = data.get("assigned_employee")
            employee = get_object_or_404(User,username = employee_username)
            client_username = data.get("client")
            client = get_object_or_404(User,username = client_username)
        except Exception as e :
            print("Error during get_object_or_404:", str(e))
            return Response({"error": "Error retrieving user information"}, status=400)

        car_data = {'registration_number':data.get("registration_number"),
            'brand':data.get("brand"),
            'model':data.get("model"),
            'status':data.get("status"),
            'assigned_employee':employee.id,  # Set the foreign key directly with the Employee instance
            'client':client.id }

        car_serializer = CarSerializer(data=car_data)
        if car_serializer.is_valid():
            car_serializer.save()
            return Response({"message": "car was added successfully."}, status=201)

        return Response(car_serializer.errors, status=400)


class CarUpdateAPIView(APIView):
    permission_classes = [IsEmployee | IsAdmin]

    def put(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            if request.user.role == 'employee':
                car.status = serializer.validated_data.get('status', car.status)
                car.save()
                return Response(serializer.data)
            elif request.user.role == 'admin':
                car = serializer
                car.save()
                return Response(serializer.data)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDeleteAPIView(APIView):
    permission_classes = [IsAdmin]  # Only admin can view details
    def delete(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDeleteAPIView(APIView):
    permission_classes = [IsAdmin]  # Only admin can view details
    def delete(self, request, username):
        print(username)
        user = get_object_or_404(User, username=username)
        print("&",user.username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarClientDetailAPIView(APIView):
    permission_classes = [IsClient]
    def get(self, request):
        car = get_object_or_404(Car, client_id=request.user.id)
        serializer = CarSerializer(car)
        car_data = {'registration_number': serializer.data.get("registration_number"),
                    'brand': serializer.data.get("brand"),
                    'model': serializer.data.get("model"),
                    'status': serializer.data.get("status"),}
        return Response(car_data)


class RegisterUSERView(APIView):
    def post(self, request):
        # Only allow employees to add clients
        if request.user.role == 'employee':
            data = request.data
            data['role'] = 'client'  # Set role to client
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "a client user was added successfully."}, status=201)

            return Response(serializer.errors, status=400)
        elif request.user.role == 'admin':
            data = request.data
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "a user was added successfully."}, status=201)
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
            return Response({'token': token})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

