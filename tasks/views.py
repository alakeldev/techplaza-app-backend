from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import logging

# Create your views here.

logger = logging.getLogger(__name__)
class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            logger.debug(f"Fetching tasks for user: {self.request.user}")
            return Task.objects.filter(user=self.request.user)
        except Exception as e:
            logger.error(f"Error fetching tasks: {e}")
            return Response({"error": "Error fetching tasks"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        try:
            logger.debug(f"Creating task for user: {self.request.user}")
            serializer.save(user=self.request.user)
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return Response({"error": "Error creating task"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)