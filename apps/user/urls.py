
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    CreateUserView, GoogleAuthView, GoogleLoginView,
    FacebookAuthView, FacebookLoginView
)

urlpatterns = [
    path('create/by_email/', csrf_exempt(CreateUserView.as_view())),
    path('complete/google-oauth2/', csrf_exempt(GoogleAuthView.as_view())),
    path('login/google-oauth2/', csrf_exempt(GoogleLoginView.as_view())),
    path('complete/facebook-oauth2/', csrf_exempt(FacebookAuthView.as_view())),
    path('login/facebook-oauth2/', csrf_exempt(FacebookLoginView.as_view())),
]
