import requests
from django.conf import settings
from oauth2client.client import OAuth2WebServerFlow


class ThirdpartyOauth:
    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"

    def __init__(self, auth_source, code, state):
        self.auth_source = auth_source
        self.code = code
        self.state = state

    def authorize(self):
        if self.auth_source == GOOGLE:
            authorize_from_google()
        elif self.auth_source == FACEBOOK:
            authorize_from_facebook()
        else:
            pass

    def get_flow_object(self):
        credentials = "credentials"
        oauth_scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid"
        ]
        self.flow = OAuth2WebServerFlow(
            settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            oauth_scopes,
            "http://127.0.0.1:8066/user/complete/google-oauth2/")

    def authenticate_g2(self):
        authorize_url = self.flow.step1_get_authorize_url()
        print(authorize_url)
        return authorize_url

    def authorize_g2(self):
        # print 'Go to the following link in your browser: ' + authorize_url
        code = self.code
        credentials = self.flow.step2_exchange(code)
        storage = Storage(credentials_file)
        storage.put(credentials)
        print('The credentials_file saved to {%s}' % credentials_file)

    def authorize_from_google(self):
        url = "https://oauth2.googleapis.com/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded,"}
        params = {
            "code": self.code,
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            "redirect_uri": "http://127.0.0.1:8066/user/complete/google-oauth2/",
            "grant_type": "authorization_code",
        }
        res = requests.post(url, headers=headers, params=params)
        return res

    def authorize_from_facebook(self):
        pass
