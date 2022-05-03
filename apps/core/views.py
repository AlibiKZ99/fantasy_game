from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response

from .models import Team, Player, Transfer, TransferHistory
from .serializers import (
    TeamSerializer,
    TeamUpdateSerializer,
    PlayerSerializer,
    TransferSerializer,
    TransferUpdateSerializer,
    TransferBuySerializer,
    TransferCreateSerializer,
    TransferHistorySerializer,
)
from .permissions import IsTransferOfOwnPlayer, IsNotTransferOfOwnPlayer


class TeamViewSet(GenericViewSet, UpdateModelMixin, ListModelMixin, RetrieveModelMixin):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    http_method_names = ("get", "post", "patch")

    def get_serializer_class(self):
        if self.action == "partial_update":
            return TeamUpdateSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes += [
                IsAdminUser,
            ]
        return super().get_permissions()

    @action(
        methods=[
            "get",
        ],
        permission_classes=[
            IsAuthenticated,
        ],
        detail=False,
    )
    def info(self, request, *args, **kwargs):
        team = request.user.team
        return Response(self.get_serializer(team).data)


class PlayerViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Player.objects.all()
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get",)
    serializer_class = PlayerSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(team__user=self.request.user)


class TransferViewSet(ModelViewSet):
    queryset = Transfer.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = TransferSerializer
    http_method_names = ("get", "post", "put", "delete")

    def get_serializer_class(self):
        if self.action == "update":
            return TransferUpdateSerializer
        if self.action == "buy":
            return TransferBuySerializer
        if self.action == "create":
            return TransferCreateSerializer
        return TransferSerializer

    def get_permissions(self):
        if self.action in ["destroy", "update"]:
            self.permission_classes = [IsAuthenticated, IsTransferOfOwnPlayer]
        if self.action in [
            "buy",
        ]:
            self.permission_classes = [IsAuthenticated, IsNotTransferOfOwnPlayer]
        if self.action in ["retrieve", ]:
            self.permission_classes = [IsAuthenticated, ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(TransferSerializer(instance).data)

    def get_queryset(self):
        return self.queryset.filter(is_sold=False)

    @action(
        methods=[
            "post",
        ],
        detail=True,
    )
    def buy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer()
        player = serializer.make_purchase(instance)
        return Response(PlayerSerializer(player).data)


class TransferHistoryViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = TransferHistory.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = TransferHistorySerializer
    http_method_names = ("get",)
