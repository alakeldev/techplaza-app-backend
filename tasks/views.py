from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated


class TaskView(viewsets.ModelViewSet):
    """
    ViewSet for managing Task objects.
    Requires authentication for all actions.
    Returns the queryset of tasks for the currently authenticated user.
    Associates the task with the currently authenticated user.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
