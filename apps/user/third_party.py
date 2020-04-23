import requests
import httplib2
import urllib.parse

from django.conf import settings

from apiclient import discovery
from oauth2client.client import OAuth2WebServerFlow

from apps.user.models import CustomUser


class ThirdpartyOauth:
    GOOGLE = CustomUser.GOOGLE
    FACEBOOK = CustomUser.FACEBOOK

    def __init__(self, auth_source, code=None):
        self.auth_source = auth_source
        self.code = code
        self.auth_url = None
        self.credentials = None
        self.user_model_object = None

        if self.auth_source == self.GOOGLE:
            self.scopes = [
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "openid"
            ]
            self.auth_key = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
            self.auth_secret = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
            self.flow = OAuth2WebServerFlow(
                self.auth_key,
                self.auth_secret,
                self.scopes,
                "http://127.0.0.1:8066/user/complete/google-oauth2/")

        elif self.auth_source == self.FACEBOOK:
            self.scopes = ["email"]
            self.auth_key = settings.SOCIAL_AUTH_FACEBOOK_OAUTH2_KEY
            self.auth_secret = settings.SOCIAL_AUTH_FACEBOOK_OAUTH2_SECRET
            FACEBOOK_AUTH_URI = "https://www.facebook.com/v6.0/dialog/oauth"
            FACEBOOK_TOKEN_URI = "https://graph.facebook.com/v6.0/oauth/access_token"
            FACEBOOK_REDIRECT_URI = "https://127.0.0.1:8443/user/complete/facebook-oauth2/"
            self.flow = OAuth2WebServerFlow(
                self.auth_key,
                self.auth_secret,
                self.scopes,
                FACEBOOK_REDIRECT_URI,
                token_uri=FACEBOOK_TOKEN_URI,
                auth_uri=FACEBOOK_AUTH_URI,
            )

    def get_auth_url(self):
        """
        * Step 1: get login URL (optional, can skip this step if already have a callback `code`)
        """

        self.auth_url = self.flow.step1_get_authorize_url()
        return self.auth_url

    def get_access_token(self, code):
        """
        * Step 2: use the callback `code` from `get_auth_url() method to get access_token
        """
        # decode url encoding
        if '%' in code:
            code = urllib.parse.unquote(code)
        self.code = code
        self.credentials = self.flow.step2_exchange(code)

    def get_user_identity(self):
        """
        * Step 3: get user identity on third party website
        """
        if not self.credentials:
            return None
        self.email = self.credentials.id_token.get('email')
        self.name = self.credentials.id_token.get('name')
        self.user_id = self.credentials.id_token.get('sub')
        self.user = self._get_or_create_user_model_object()
        return self.user

    def _get_or_create_user_model_object(self):
        user, created = CustomUser.objects.get_or_create(
            email=self.email,
            third_party_id=self.user_id,
            last_name=self.name,
            registered_source=self.auth_source,
        )
        return user
