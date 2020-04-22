import json
import logging
import traceback

from django.views import View
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from social_core.actions import do_complete
from social_django.models import UserSocialAuth

from apps.user.models import CustomUser, UserValidator
from apps.user.schema import Userchema
from apps.core.mail import send_email_with_mailgun

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
        except:
            response.status_code = 500
            logger.debug(str(traceback.format_exc))
            response_msg = {"error": "Something went wrong."}

        response.content = json.dumps(response_msg)

        return response


class ThirdPartyAuthView(APIView):
    permission_classes = []

    def post(self, request, backend, *args, **kwargs):
        result = do_complete(request, backend, *args, **kwargs)

        response = Response()
        token = UserSocialAuth.objects.get(user=None)
        response.content = json.dump({"token": token})
