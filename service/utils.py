from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class SimulatedUser:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email

    @property
    def is_authenticated(self):
        return True


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = self.get_raw_token(self.get_header(request))
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user_id = validated_token.get("user_id")
        username = validated_token.get("username", "Unknown User")
        email = validated_token.get("email", "")

        if not user_id:
            raise AuthenticationFailed("User ID not found in token.")

        # Return a SimulatedUser object
        user = SimulatedUser(user_id=user_id, username=username, email=email)
        return user, validated_token
