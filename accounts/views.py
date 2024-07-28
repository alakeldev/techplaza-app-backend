from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.core.mail import send_mail
import random
import string

# Create your views here.

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer=self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data

            otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            send_mail(
                'OTP for Registration Verification',
                f'Your OTP for registration verification is {otp}.',
                'techplaza1@hotmail.com',
                [user['email']],
                fail_silently=False,
            )

            return Response({
                'data':user,
                'message':f'Thanks for your Registration 
                {user.full_name}, a verified code has been sent to your Email.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST)