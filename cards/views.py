from django.shortcuts import render
from rest_framework import viewsets
from .models import Card
from .serializers import CardSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)