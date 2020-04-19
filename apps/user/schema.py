from rest_framework import serializers

from apps.user.models import CustomUser


class Userchema(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'
