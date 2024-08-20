from rest_framework import serializers
from .models import HighScore
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ["email", "full_name"]


class HighScoreSerializer(serializers.ModelSerializer):
    """
    Serializer for the HighScore model.
    Includes nested user information.
    """

    user = UserSerializer(read_only=True)

    class Meta:
        model = HighScore
        fields = ["id", "user", "score"]
