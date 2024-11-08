from django.urls import path
from .views import CarCreateAPIView, CarDetailAPIView, CarUpdateAPIView, CarDeleteAPIView, \
    UserLoginAPIView, CarLISTAPIView, CarClientDetailAPIView, RegisterUSERView, UserDeleteAPIView

urlpatterns = [
    path('car/<str:immatriculation>/', CarDetailAPIView.as_view(), name='car-view'),
    path('cars/', CarLISTAPIView.as_view(), name='car-list-view'),
    path('car/add', CarCreateAPIView.as_view(), name='add-car'),
    path('cars/<str:immatriculation>/update/', CarUpdateAPIView.as_view(), name='car-update'),
    path('cars/<str:immatriculation>/delete/', CarDeleteAPIView.as_view(), name='car-delete'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('client/', CarClientDetailAPIView.as_view(), name='Client-car'),
    path('user/register/', RegisterUSERView.as_view(), name='user-register'),
    path('user/<str:username>/delete/', UserDeleteAPIView.as_view(), name='user-delete'),

]
