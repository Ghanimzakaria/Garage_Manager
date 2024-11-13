# tests/test_car_views.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from cars.models import Car, User




@pytest.mark.django_db
def test_car_detail_view():
    client = APIClient()
    admin_user = User.objects.create_user(username="manager_zak", password="ziko", role="admin")
    client.force_authenticate(user=admin_user)

    car = Car.objects.create(registration_number="ABC123", brand="Toyota", model="Corolla",
                             status="in_progress")

    response = client.get(reverse('car-view', args=[car.registration_number]))
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["brand"] == "Toyota"
    assert response.data["model"] == "Corolla"

@pytest.mark.django_db
def test_car_list_view():
    client = APIClient()
    admin_user = User.objects.create_user(username="manager_zak", password="ziko", role="admin")
    client.force_authenticate(user=admin_user)

    Car.objects.create(registration_number="ABC123", brand="Toyota", model="Corolla", status="in_progress")
    Car.objects.create(registration_number="XYZ789", brand="Honda", model="Civic", status="completed")

    response = client.get(reverse('car-list-view'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

@pytest.mark.django_db
def test_create_car_view():
    client = APIClient()
    admin_user = User.objects.create_user(username="manager_zak", password="ziko", role="admin")
    employee_user = User.objects.create_user(username="employee1", password="ziko", role="employee")
    client_user = User.objects.create_user(username="Clien1", password="ziko", role="client")
    client.force_authenticate(user=admin_user)

    data = {
        "registration_number": "NEW123",
        "brand": "Ford",
        "model": "Focus",
        "status": "in_progress",
        "assigned_employee": employee_user.username,
        "client": client_user.username
    }
    response = client.post(reverse('add-car'), data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "car was added successfully."

@pytest.mark.django_db
def test_create_car_deniyed_for_client_view():
    client = APIClient()
    client_user = User.objects.create_user(username="Clien2", password="ziko", role="client")
    client.force_authenticate(user=client_user)

    data = {
        "registration_number": "NEW123",
        "brand": "Ford",
        "model": "Focus",
        "status": "in_progress",

    }
    response = client.post(reverse('add-car'), data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_car_view():
    client = APIClient()
    admin_user = User.objects.create_user(username="manager_zak", password="ziko", role="admin")
    client.force_authenticate(user=admin_user)

    car = Car.objects.create(registration_number="UPDATE123", brand="Nissan", model="Altima", status="in_progress")

    data = {"status": "completed","brand" : "BMW"}
    response = client.put(reverse('car-update', args=[car.registration_number]), data, format='json')
    assert response.status_code == status.HTTP_200_OK
    car.refresh_from_db()
    assert car.status == "completed"
    assert car.brand == "BMW"


@pytest.mark.django_db
def test_update_car_employee_view():
    client = APIClient()
    employee_user = User.objects.create_user(username="employee1", password="ziko", role="employee")
    client.force_authenticate(user=employee_user)

    car = Car.objects.create(registration_number="UPDATE123", brand="Nissan", model="Altima", status="in_progress")

    data = {"status": "completed", "brand": "BMW"}
    response = client.put(reverse('car-update', args=[car.registration_number]), data, format='json')

    assert response.status_code == status.HTTP_200_OK
    car.refresh_from_db()
    assert car.status == "completed"
    assert car.brand == "Nissan"


@pytest.mark.django_db
def test_delete_car_view():
    client = APIClient()
    admin_user = User.objects.create_user(username="manager_zak", password="ziko", role="admin")
    client.force_authenticate(user=admin_user)

    car = Car.objects.create(registration_number="DELETE123", brand="BMW", model="3 Series", status="in_progress")

    response = client.delete(reverse('car-delete', args=[car.registration_number]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Car.objects.filter(registration_number="DELETE123").count() == 0
