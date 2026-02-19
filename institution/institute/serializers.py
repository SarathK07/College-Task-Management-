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
        fields = ("username", "password", "role")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            role="trainer"
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "role")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            role="student"
        )
        user.set_password(validated_data["password"])
        user.save()
        return user





