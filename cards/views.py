from rest_framework import viewsets
from .models import Card
from .serializers import CardSerializer
from rest_framework.permissions import IsAuthenticated


class CardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Card objects.
    Requires authentication for all actions
    Associates the card with the currently authenticated user.
    """

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
