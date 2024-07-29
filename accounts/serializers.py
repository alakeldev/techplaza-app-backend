from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(max_length=40, min_length=4, write_only=True)
    password2=serializers.CharField(max_length=40, min_length=4, write_only=True)

    class Meta:
        model=User
        fields=['full_name', 'email', 'password1', 'password2']

    def validate(self, attrs):
        password1 = attrs.get('password1', '')
        password2 = attrs.get('password2', '')
        if password1 != password2:
            raise serializers.ValidationError("The password fields didn't match")
        else:
            return attrs
    

    def create(self, validated_data):
        user=User.objects.create_user(
            full_name=validated_data.get('full_name'),
            email=validated_data.get('email'),
            password=validated_data.get('password1'),
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=10)
    password=serializers.CharField(max_length=40, min_length=4, write_only=True)
    full_name=serializers.CharField(max_length=100, read_only=True)
    token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model=User
        fields=['email', 'password', 'full_name', 'token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Sorry the cerdentials are invalid")
        else:
            return {
                'full_name': user.user_full_name,
                'email': user.email,
            }
