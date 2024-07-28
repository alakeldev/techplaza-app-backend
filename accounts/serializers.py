from rest_framework import serializers
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