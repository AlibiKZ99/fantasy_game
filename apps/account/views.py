from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from .models import Activation
from .serializers import (
    ActivationCreateSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    RegistrationSerializer,
    ForgotPasswordSerializer,
    UserSerializer,
)

from utils import messages, constants


class LoginViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class ChangePasswordViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class ForgotPasswordViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer


class ActivationViewSet(GenericViewSet, CreateModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = ActivationCreateSerializer
    queryset = Activation.objects.all()
    lookup_url_kwarg = constants.UUID_FIELD
    lookup_field = constants.UUID_FIELD

    def get_serializer_class(self):
        if self.action == "activate":
            return RegistrationSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": messages.ACTIVATION_CODE_IS_SENT})

    @action(
        detail=True,
        methods=[
            "get",
        ],
        permission_classes=[
            AllowAny,
        ],
    )
    def activate(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.complete(instance)
        return Response(UserSerializer(user).data)
