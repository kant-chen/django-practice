from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from apps.core.mail import send_email_with_mailgun
from apps.core.models import Base


class UserValidator:
    ERROR_EMAIL_EXIST = "The email address: {} is already exist."
    ERROR_EMAIL_FORMAT = "The format of email address: {} is not correct."
    ERROR_PASSWORD_NOT_THE_SAME = "Passwords and retyped passwords is not the same."
    ERROR_PASSWORD_MINIMUM_LENGTH = "Minimum password length is 8."

    @classmethod
    def is_email_exist(cls, email):
        # check exist
        count = CustomUser.objects.filter(email=email).count()
        if count >= 1:
            raise ValidationError(cls.ERROR_EMAIL_EXIST.format(email))
        # verify format
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(cls.ERROR_EMAIL_FORMAT.format(email))

    @classmethod
    def compare_password(cls, password, password_retype):
        if password != password_retype:
            raise ValidationError(cls.ERROR_PASSWORD_NOT_THE_SAME)

        if len(password) < 8:
            raise ValidationError(cls.ERROR_PASSWORD_MINIMUM_LENGTH)


class CustomUser(AbstractUser, Base):
    EMAIL = 1
    GOOGLE = 2
    FACEBOOK = 3
    REGISTERED_SOURCE_CHOICES = (
        (EMAIL, 'EMAIL'),
        (GOOGLE, 'GOOGLE'),
        (FACEBOOK, 'FACEBOOK'),
    )
    email = models.EmailField(blank=True, unique=True,
                              validators=[validate_email, UserValidator.is_email_exist])
    third_party_id = models.CharField(max_length=100, null=True)
    registered_source = models.IntegerField(
        default=EMAIL, choices=REGISTERED_SOURCE_CHOICES)

    def send_email_after_register(self):
        sender = [self.email]
        subject = "Welcome to Amazing Talker"
        text = "Hi {}:\nWelcome to join!\n\nRegards,\nAmazing Talker Team"
        send_email_with_mailgun(sender, subject, text)

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def do_actions_after_user_create(sender, instance=None, created=False, **kwargs):
    if created:
        from apps.wallet.models import Coupon
        instance.send_email_after_register()
        Token.objects.create(user=instance)
        Coupon.create_user_registered_coupon(user=instance)
