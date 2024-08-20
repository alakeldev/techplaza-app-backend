from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
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

    def high(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized access. Please provide valid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().high(request, *args, **kwargs)