from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Car,User
from .permissions import IsAdmin, IsEmployee, IsClient
from .serializers import CarSerializer, UserSerializer, UsershowSerializer


# Récupérer les détails d'une voiture par son immatriculation
class CarDetailAPIView(APIView):

    permission_classes = [IsAdmin]

    def get(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        serializer = CarSerializer(car)
        IsAdmin.get_session_data(request)
        return Response(serializer.data)


class CarLISTAPIView(APIView):
    permission_classes = [IsEmployee | IsAdmin]

    def get(self, request):
        if request.user.role == 'admin':
            cars = Car.objects.all()
            serializers = CarSerializer(cars, many=True)
            for ser, car in enumerate(cars):
                employee = get_object_or_404(User, id=serializers.data[ser].get('assigned_employee'))
                client = get_object_or_404(User, id=serializers.data[ser].get('client'))
                serializers.data[ser]['assigned_employee'] = employee.username
                serializers.data[ser]['client'] = client.username
            return Response(serializers.data)

        elif request.user.role == 'employee':
            cars = get_list_or_404(Car, assigned_employee=request.user.id)
            serializers = CarSerializer(cars, many=True)
            return Response(serializers.data)

class CarCreateAPIView(APIView):
    permission_classes = [IsAdmin]

    def post(self,request):
        data = request.data
        try:
            employee_username = data.get("assigned_employee")
            employee = get_object_or_404(User,username=employee_username)
            client_username = data.get("client")
            client = get_object_or_404(User,username=client_username)
        except Exception as e :
            print("Error during get_object_or_404:", str(e))
            return Response({"error": "Error retrieving user information"}, status=400)

        car_data = {'registration_number':data.get("registration_number"),
            'brand':data.get("brand"),
            'model':data.get("model"),
            'status':data.get("status"),
            'assigned_employee':employee.id,
            'client':client.id}

        car_serializer = CarSerializer(data=car_data)
        if car_serializer.is_valid():
            car_serializer.save()
            return Response({"message": "car was added successfully."}, status=201)

        return Response(car_serializer.errors, status=400)


class CarUpdateAPIView(APIView):
    permission_classes = [IsEmployee | IsAdmin]

    def put(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        data = request.data
        serializerx = CarSerializer(car, partial=True)


        if request.user.role == 'employee':

            car.status = data.get('status', car.status)
            serializer_emp = CarSerializer(car,partial=True)
            car.save()
            return Response(serializer_emp.data)
        elif request.user.role == 'admin':
            try:
                employee_username = data.get("assigned_employee")
                employee = get_object_or_404(User, username=employee_username)
                client_username = data.get("client")
                client = get_object_or_404(User, username=client_username)
            except Exception as e:
                print("Error during get_object_or_404:", str(e))
                return Response({"error": "Error retrieving user information"}, status=400)
            car_data = {'registration_number': data.get("registration_number"),
                        'brand': data.get("brand"),
                        'model': data.get("model"),
                        'status': data.get("status"),
                        'assigned_employee': employee.id,
                        'client': client.id}
            serializer = CarSerializer(car, data=car_data, partial=True)
            if serializer.is_valid() :
                car = serializer
                car.save()
            return Response(serializer.data)


        else :
                return Response(serializerx.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDeleteAPIView(APIView):
    permission_classes = [IsAdmin]  # Only admin can view details
    def delete(self, request, immatriculation):
        car = get_object_or_404(Car, registration_number=immatriculation)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDeleteAPIView(APIView):
    permission_classes = [IsAdmin]  # Only admin can view details
    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarClientDetailAPIView(APIView):
    permission_classes = [IsClient]
    def get(self, request):
        car = get_list_or_404(Car, client_id=request.user.id)
        serializer = CarSerializer(car, many=True)
        return Response(serializer.data)


class RegisterUSERView(APIView):
    permission_classes = [IsAdmin]
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
    def get(self, request):
        users = User.objects.all()
        serializer = UsershowSerializer(users, many=True)
        return Response(serializer.data)






class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate( username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'role': user.role  # Assuming the user model has a 'role' field
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)