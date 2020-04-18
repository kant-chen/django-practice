from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy


class UserValidator:
    @staticmethod
    def is_email_exist(cls, email):
        exist = False
        count = CustomUser.objects.filter(email=email).count()
        if count >= 1:
            exist = True
            raise ValidationError(ERROR_EMAIL_EXIST.format(email))


class CustomUser(AbstractUser):
    EMAIL = 1
    GOOGLE = 2
    FACEBOOK = 3
    REGISTERED_SOURCE_CHOICES = (
        (EMAIL, 'EMAIL'),
        (GOOGLE, 'GOOGLE'),
        (FACEBOOK, 'FACEBOOK'),
    )
    ERROR_EMAIL_EXIST = "The email {} is already exist."
    email = models.EmailField(blank=True, unique=True,
                              validators=[validate_email, UserValidator.is_email_exist])
    third_party_id = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registered_source = models.IntegerField(
        default=EMAIL, choices=REGISTERED_SOURCE_CHOICES)
