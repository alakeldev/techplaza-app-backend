from rest_framework import serializers
from .models import Card

class CardSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Card
        fields = ['id', 'email', 'name', 'phone_number', 'profession', 'description', 'country']