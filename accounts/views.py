from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import timedelta
import random
import string
from .serializers import RegisterSerializer, LoginSerializer, PasswordResetSerializer, NewPasswordSerializer
from .models import User

# Create your views here.

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer=self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            send_mail(
                'OTP for Registration Verification',
                f'Your OTP for registration verification is {otp}.',
                'techplaza1@hotmail.com',
                [user.email],
                fail_silently=False,
            )

            user_data = RegisterSerializer(user).data

            return Response({
                'data':user_data,
                'message': f'''Thanks for your Registration {user.full_name},
                            a verified code has been sent to your Email.'''
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST)
    

class VerifyEmail(APIView):
    def post(self, request):
        otp_to_verify = request.data.get('otp')
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            otp_valid_duration = 15  

            if user.otp == otp_to_verify and timezone.now() - user.otp_created_at <= timedelta(minutes=otp_valid_duration):
                user.is_verified = True
                user.save()
                return Response({
                    'message': 'Email successfully verified'
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'error': 'Invalid or expired OTP.'
                }, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({
                'error': 'User does not exist / OTP not provided'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'A reset link sent to your email, check the spam email please'}, status=status.HTTP_200_OK)
    

class ConfirmPasswordResetView(GenericAPIView):
    def get(self,request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'Token is expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'The credentials are valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'message': 'token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        

class NewPasswordView(GenericAPIView):
    serializer_class = NewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message' : 'Your Password Reset Successfully'}, status=status.HTTP_200_OK)