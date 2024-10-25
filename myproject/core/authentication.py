from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken
from accounts.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)

        if not auth:
            return None
        try:
            token_type, token = auth.split()
            if token_type != 'Bearer':
                return None

            payload = UntypedToken(token).payload
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            return (user, None)

        except Exception as e:
            raise AuthenticationFailed('Invalid token or user does not exist') from e