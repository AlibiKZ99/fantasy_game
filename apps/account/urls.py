from django.urls import path, include

from rest_framework import routers
from .views import (
    ActivationViewSet,
    LoginViewSet,
    ChangePasswordViewSet,
    ForgotPasswordViewSet,
)


app_name = "account"

router = routers.DefaultRouter()
router.register(r"activation", ActivationViewSet, basename="activation")
router.register(r"login", LoginViewSet, basename="login")
router.register(r"change_password", ChangePasswordViewSet, basename="change_password")
router.register(r"forgot_password", ForgotPasswordViewSet, basename="forgot_password")

urlpatterns = [
    path("", include(router.urls)),
]
