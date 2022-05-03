import jwt
import uuid
from utils import (
    constants,
    messages,
)

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = constants.EMAIL_FIELD
    REQUIRED_FIELDS = [
        constants.USERNAME_FIELD,
    ]

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=constants.JWT_TOKEN_LIFETIME)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm=constants.JWT_ALGORITHM,
        )

        return token


class ActivationManager(models.Manager):
    def create(self, email, password):
        activation = self.model(email=email)
        activation.end_time = timezone.now() + timedelta(
            minutes=constants.ACTIVATION_TIME
        )
        activation.password = password
        activation.save()
        return activation


class Activation(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    end_time = models.DateTimeField(blank=True, null=True)
    objects = ActivationManager()

    def is_valid(self, raise_exception=False):
        if self.end_time < timezone.now():
            self.is_active = False
            self.save()
            if raise_exception:
                raise ValidationError(messages.LINK_EXPIRED)
            return False, messages.LINK_EXPIRED
        if not self.is_active:
            if raise_exception:
                raise ValidationError(messages.LINK_INACTIVE)
            return False, messages.LINK_INACTIVE
        return True, None

    def __str__(self):
        return f"{self.email}, {self.is_active}"
