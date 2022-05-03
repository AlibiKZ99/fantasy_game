import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User
from utils import messages, constants


def _authenticate_credentials(token):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=constants.JWT_ALGORITHM
        )
    except Exception:
        error = messages.AUTHENTICATION_ERROR
        raise exceptions.AuthenticationFailed(error)

    try:
        user = User.objects.get(pk=payload["id"])
    except User.DoesNotExist as error:
        raise exceptions.AuthenticationFailed(error)

    if not user.is_active:
        error = messages.NONE_ACTIVE_USER
        raise exceptions.AuthenticationFailed(error)

    return user, token


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Token"

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None
        elif len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != auth_header_prefix:
            return None

        return _authenticate_credentials(token)
