"""
JWT Authentication for auth_app.
"""
import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import exceptions
from datetime import datetime, timedelta


class JWTAuthentication:
    """Custom JWT authentication class."""

    @staticmethod
    def generate_token(user):
        """Generate JWT token for user."""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow(),
        }
        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        return token

    @staticmethod
    def verify_token(token):
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

    def authenticate(self, request):
        """Authenticate user from JWT token in Authorization header."""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header[7:]  # Remove 'Bearer ' prefix
        
        try:
            payload = self.verify_token(token)
            user = User.objects.get(id=payload['user_id'])
            return (user, token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
