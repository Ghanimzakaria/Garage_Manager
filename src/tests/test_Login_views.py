import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from cars.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="testpass", role="client")


@pytest.mark.django_db
def test_user_login_success(api_client, test_user):
    # Prepare login data
    url = reverse('login')  # Replace with the actual URL name for UserLoginAPIView
    data = {"username": "testuser", "password": "testpass"}

    # Send login request
    response = api_client.post(url, data, format='json')

    # Verify successful login response
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data


@pytest.mark.django_db
def test_user_login_invalid_credentials(api_client):
    # Prepare invalid login data
    url = reverse('login')  # Replace with the actual URL name for UserLoginAPIView
    data = {"username": "wronguser", "password": "wrongpass"}

    # Send login request
    response = api_client.post(url, data, format='json')

    # Verify login failure due to invalid credentials
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Invalid credentials"
