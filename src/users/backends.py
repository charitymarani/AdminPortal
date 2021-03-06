import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import CustomUser


class JWTAuthentication(authentication.BaseAuthentication):
    """Class to override default authentication
    and use custom token based authentication
    """

    def authenticate(self, request):
        """This method authenticates the token and the provided credentials"""

        auth_header = authentication.get_authorization_header(
            request).decode('utf-8')

        if not auth_header or auth_header.split()[0].lower() != 'token':
            return None
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")
            user = CustomUser.objects.get(email=payload['email'], is_active=True)
            if not user:
              raise exceptions.AuthenticationFailed("User does not exist")

        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")
       
        return user, token
