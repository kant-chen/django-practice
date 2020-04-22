
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from .views import CreateUserView, GoogleAuthView, GoogleLoginView

urlpatterns = [
    path('create/by_email/', csrf_exempt(CreateUserView.as_view())),
    path('complete/google-oauth2/', csrf_exempt(GoogleAuthView.as_view())),
    path('login/google-oauth2/', csrf_exempt(GoogleLoginView.as_view())),
]
