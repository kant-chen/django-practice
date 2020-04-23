import json
import logging
import traceback

from django.views import View
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse

from oauth2client.client import FlowExchangeError
from social_core.actions import do_complete
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.user.models import CustomUser, UserValidator
from apps.user.schema import Userchema
from apps.core.mail import send_email_with_mailgun
from apps.user.third_party import ThirdpartyOauth
from rest_framework.authtoken.models import Token

logger = logging.getLogger()


class CreateUserView(APIView):
    permission_classes = []

    def post(self, request):
        response = Response()
        response_msg = None
        data = json.loads(request.body).get('data')
        try:
            UserValidator.compare_password(
                data.get('password'), data.get('password_retype'))
            fields = ['email', 'last_name']
            data = {key: value for key, value in data.items() if key in fields}
            user = CustomUser(**data)
            user.set_password(user.password)
            user.save()
            response.status_code = 201
            token = user.auth_token.key
            response_msg = {"token": token}
        except ValidationError as e:
            response.status_code = 400
            response_msg = {"error": e.message}
        except IntegrityError as e:
            if "user_customuser_username_key" in e.args[0]:
                response.status_code = 400
                response_msg = {
                    "error": UserValidator.ERROR_EMAIL_EXIST.format(data.get('email'))}

        response.content = json.dumps(response_msg)

        return response


class GoogleAuthView(APIView):
    permission_classes = []
    INVALID_AUTH_CODE = "Invalid authorize_code"

    def get(self, request):
        response = Response()
        response_msg = None
        error = request.GET.get('error', '')
        'access_denied'
        auth = ThirdpartyOauth(ThirdpartyOauth.GOOGLE)
        code = request.GET.get('code', '')
        try:
            auth.get_access_token(code)
            user_model_object = auth.get_user_identity()
            token = Token.objects.get(user=user_model_object).key
            response_msg = {"token": token}
            response.status_code = 200
        except FlowExchangeError as e:
            response_msg = {"error": self.INVALID_AUTH_CODE}
            response.status_code = 400

        response.content = json.dumps(response_msg)

        return response


class FacebookAuthView(APIView):
    permission_classes = []
    INVALID_AUTH_CODE = "Invalid authorize_code"

    def get(self, request):
        response = Response()
        response_msg = None
        error = request.GET.get('error', '')
        'access_denied'
        auth = ThirdpartyOauth(ThirdpartyOauth.FACEBOOK)
        code = request.GET.get('code', '')
        try:
            auth.get_access_token(code)
            user_model_object = auth.get_user_identity()
            token = Token.objects.get(user=user_model_object).key
            response_msg = {"token": token}
            response.status_code = 200
        except FlowExchangeError as e:
            response_msg = {"error": self.INVALID_AUTH_CODE}
            response.status_code = 400

        response.content = json.dumps(response_msg)

        return response


class GoogleLoginView(APIView):
    permission_classes = []

    def get(self, request):
        response = Response()
        auth = ThirdpartyOauth(ThirdpartyOauth.GOOGLE)
        url = auth.get_auth_url()

        return redirect(url)


class FacebookLoginView(APIView):
    permission_classes = []

    def get(self, request):
        response = Response()
        auth = ThirdpartyOauth(ThirdpartyOauth.FACEBOOK)
        url = auth.get_auth_url()

        return redirect(url)
