from django.shortcuts import render
from rest_framework import viewsets
from .models import HighScore
from .serializers import HighScoreSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class HighScoreViewSet(viewsets.ModelViewSet):
    serializer_class = HighScoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HighScore.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)