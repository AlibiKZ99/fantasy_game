from rest_framework import permissions


class IsTransferOfOwnPlayer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        val = obj.player.team.user == request.user
        return val


class IsNotTransferOfOwnPlayer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.player.team.user != request.user
