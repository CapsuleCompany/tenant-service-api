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

    def __str__(self):
        return self.username


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the header from the request
        header = self.get_header(request)
        if header is None:  # Handle missing header
            return None

        # Get the raw token from the header
        raw_token = self.get_raw_token(header)
        if raw_token is None:  # Handle missing token
            return None

        try:
            # Validate the token
            validated_token = self.get_validated_token(raw_token)
        except AuthenticationFailed as exc:
            raise AuthenticationFailed(f"Token validation failed: {str(exc)}")

        # Extract user information from the validated token
        user_id = validated_token.get("user_id")
        username = validated_token.get("username", "Unknown User")
        email = validated_token.get("email", "")

        if not user_id:
            raise AuthenticationFailed("User ID not found in token.")

        # Create and return the user and token
        user = SimulatedUser(user_id=user_id, username=username, email=email)
        return user, validated_token
