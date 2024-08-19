from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(_("Full Name"), max_length=100)
    email = models.EmailField(_("Email Address"), max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    
    REQUIRED_FIELDS = ["full_name",]

    objects = UserManager()

    def __str__(self):
        return self.email

    def user_full_name(self):
        return self.full_name

    def user_tokens(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh_token': str(refresh),
            'token': str(refresh.access),
        }