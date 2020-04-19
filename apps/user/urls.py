from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import CreateUserView

urlpatterns = [
    #path('create/third_party<int:third_party_id>', ),
    path('create/by_email/', csrf_exempt(CreateUserView.as_view())),
]
