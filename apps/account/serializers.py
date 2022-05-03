import datetime

from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from utils import messages, tools
from .models import User, Activation
from .tasks import forgot_password_task, create_team_for_user, send_code_to_email


class RegistrationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = Activation
        fields = ["email", "token"]

    @transaction.atomic()
    def complete(self, instance):
        instance.is_active = False
        instance.save()

        user = User.objects.create_user(
            email=instance.email, password=instance.password
        )

        create_team_for_user.delay(user.id)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=8)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        user = authenticate(email=email, password=password)

        if user is None:
            raise ValidationError(messages.INCORRECT_PASSWORD_OR_USER)

        if not user.is_active:
            raise ValidationError(messages.NONE_ACTIVE_USER)

        return {"email": user.email, "token": user.token}

    def create(self, validated_data):
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "token")


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    new_password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    new_password_confirm = serializers.CharField(
        max_length=255, min_length=8, write_only=True
    )
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "old_password",
            "new_password",
            "new_password_confirm",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    message = serializers.CharField(read_only=True)

    def create(self, validated_data):
        email = self.validated_data["email"]
        new_password = tools.get_random_password()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as error:
            return {"message": str(error)}
        user.set_password(new_password)
        user.save()
        forgot_password_task.delay(self.validated_data["email"], new_password)
        return {"message": messages.FORG0T_PASSWORD_SUCCESS}


class ActivationCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Activation
        fields = ("email", "password", "password_confirm")

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise ValidationError(messages.USER_EXISTS)
        if Activation.objects.filter(
            email=attrs["email"], is_active=True, end_time__gt=datetime.datetime.now()
        ).exists():
            raise ValidationError(messages.ACTIVATION_CODE_IS_SENT)
        if attrs.get("new_password") != attrs.get("new_password_confirm"):
            raise ValidationError(messages.PASSWORDS_DO_NOT_MATCH)
        return attrs

    def create(self, validated_data):
        activation = Activation.objects.create(
            email=self.validated_data["email"], password=self.validated_data["password"]
        )

        send_code_to_email.delay(
            email=activation.email,
            uuid=str(activation.uuid),
            path=str(get_current_site(self.context["request"])),
            url="activate",
        )

        return activation
