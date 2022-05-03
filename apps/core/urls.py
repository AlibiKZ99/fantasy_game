from django.urls import path, include

from rest_framework import routers
from .views import TeamViewSet, PlayerViewSet, TransferViewSet


app_name = "core"

router = routers.DefaultRouter()
router.register(r"team", TeamViewSet, basename="team")
router.register(r"player", PlayerViewSet, basename="player")
router.register(r"transfer", TransferViewSet, basename="transfer")

urlpatterns = [
    path("", include(router.urls)),
]
