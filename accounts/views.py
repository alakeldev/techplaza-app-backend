from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random
import string
from .serializers import RegisterSerializer
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