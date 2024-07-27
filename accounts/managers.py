from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please Enter Your Email"))
        
    def create_user(self, email, full_name, password, **kwrgs):
        if email:
            email=self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("a Valid Email Address is Required"))
        if not full_name:
            raise ValueError(_("Your Full Name is Required"))
        user=self.model(email=email, full_name=full_name, **kwrgs)
        user.set_password(password)
        user.save(using=self._db)
        return user