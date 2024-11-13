import pytest
from django.urls import reverse
from rest_framework import status
from cars.models import User
from rest_framework.test import APIClient


@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username="admin_user", password="adminpass", role="admin")
    return user


@pytest.fixture
def regular_user(db):
    user = User.objects.create_user(username="regular_user", password="userpass", role="employee")
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_user_view_as_admin(api_client,admin_user):
    api_client.force_authenticate(user=admin_user)

    data = {"username": "new_client", "password": "password", "role": "client"}
    response = api_client.post(reverse('user-register'), data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "a user was added successfully."
    assert User.objects.filter(username="new_client").exists()


@pytest.mark.django_db
def test_user_delete_by_admin(api_client, admin_user, regular_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('user-delete', args=[regular_user.username])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(User.DoesNotExist):
        User.objects.get(username=regular_user.username)


@pytest.mark.django_db
def test_user_delete_by_non_admin(api_client, regular_user):

    api_client.force_authenticate(user=regular_user)

    url = reverse('user-delete', args=[regular_user.username])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


