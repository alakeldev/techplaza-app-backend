from rest_framework import serializers
from .models import HighScore
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name']

class HighScoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = HighScore
        fields = ['id', 'user', 'score']