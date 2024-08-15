from django.urls import path
from .views import CardViewSet

urlpatterns = [
    path('cards/', CardViewSet.as_view({'get': 'list', 'post': 'create'}), name='cards'),
    path('cards/<int:pk>/', CardViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='card_detail'),
]