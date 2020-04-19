from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import requests
from amazingtalker.settings import (
    EMAIL_HOST_USER_NAME, EMAIL_MAILGUN_API_KEY, EMAIL_HOST_USER,
    EMAIL_HOST
)

MAILGUN_API_URL = "https://api.mailgun.net/v3/sandbox07b966bce9634412b2a2ace7e90e6437.mailgun.org"


def send_email_with_mailgun(to_addresses, subject=None, text=None):
    """To send email via MailGun API service"""

    return requests.post(
        MAILGUN_API_URL,
        auth=("api", EMAIL_MAILGUN_API_KEY),
        data={"from": "{} <{}>".format(EMAIL_HOST_USER_NAME, EMAIL_HOST_USER),
              "to": to_addresses,
              "subject": subject,
              "text": text})
