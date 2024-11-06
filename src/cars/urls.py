from django.urls import path
from .views import CarListCreateAPIView, CarDetailAPIView, CarUpdateAPIView, CarDeleteAPIView

urlpatterns = [
    path('cars/', CarListCreateAPIView.as_view(), name='car-list-create'),  # Accepte GET pour la liste et POST pour créer
    path('cars/<str:immatriculation>/', CarDetailAPIView.as_view(), name='car-detail'),
    path('cars/<str:immatriculation>/update/', CarUpdateAPIView.as_view(), name='car-update'),
    path('cars/<str:immatriculation>/delete/', CarDeleteAPIView.as_view(), name='car-delete'),
]
