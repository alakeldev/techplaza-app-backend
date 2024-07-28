from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(max_length=40, min_length=4, write_only=True)
    password2=serializers.CharField(max_length=40, min_length=4, write_only=True)

    class Meta:
        model=User
        fields=['full_name', 'email', 'password1', 'password2']
