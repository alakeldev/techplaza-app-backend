from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
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
        if not user.is_verified:
            raise AuthenticationFailed("User's Email isn't verified")
        user_token = user.user_tokens()
        return {
                'full_name': user.user_full_name,
                'email': user.email,
                'token':str(user_token.get('token')),
                'refresh_token': str(user_token.get('refresh')),
            }

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):

        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request=self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('confirm-password-reset', kwargs={'uidb64': uidb64, 'token' : token})
            absolute_link = f"http://{site_domain}{relative_link}"
            data = {
                'email_subject' : "Link to reset your password",
                'email_text' : f"Hello, please use the link below to reset the password \n {absolute_link}",
                'to': user.email
            }

            def send_email(data):
                email = EmailMessage(
                subject = data['email_subject'],
                body = data['email_text'],
                from_email = settings.EMAIL_HOST_USER,
                to = [data['to']]
                )
                email.send()
            
            send_email(data)
        return super().validate(attrs)


class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=40, min_length=4, write_only=True)
    password_confirm = serializers.CharField(max_length=40, min_length=4, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ["password", "password_confirm", "uidb64", "token"]

    def validate(self, attrs):

        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            password_confirm = attrs.get('password_confirm')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The link is invalid", 401)

            if password != password_confirm:
                raise AuthenticationFailed("Password Fields didn't match!")
            
            user.set_password(password)
            user.save()
            return user
        
        except:
            return AuthenticationFailed("The link is invalid/expired")
        

class LogoutSerializer(serializers.Serializer):
    refersh_token = serializers.CharField()
    
    default_error_messages = {
        'bad_token':('Token expired')
    }
    
    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        

class UpdateAccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        else:
            return value
        
class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'date_joined', 'last_login']