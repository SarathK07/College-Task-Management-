from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "role")


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","password","role")
        

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","password","role")




