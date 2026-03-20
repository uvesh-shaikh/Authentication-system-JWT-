"""
Views for auth_app - Authentication endpoints.
"""
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .authentication import JWTAuthentication
from .models import UserProfile


@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """
    Register a new user.
    
    POST /api/register
    {
        "username": "user123",
        "email": "user@example.com",
        "password": "securePassword123"
    }
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validation
        if not all([username, email, password]):
            return JsonResponse({
                'success': False,
                'error': 'Username, email, and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 6:
            return JsonResponse({
                'success': False,
                'error': 'Password must be at least 6 characters'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'error': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create user with hashed password
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )

        # Create user profile
        UserProfile.objects.create(user=user)

        return JsonResponse({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """
    Login user and return JWT token.
    
    POST /api/login
    {
        "username": "user123",
        "password": "securePassword123"
    }
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Validation
        if not all([username, password]):
            return JsonResponse({
                'success': False,
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Find user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Verify password
        if not check_password(password, user.password):
            return JsonResponse({
                'success': False,
                'error': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT token
        jwt_auth = JWTAuthentication()
        token = jwt_auth.generate_token(user)

        return JsonResponse({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_http_methods(["GET"])
def profile(request):
    """
    Get authenticated user's profile.
    Requires: Authorization header with Bearer token
    
    GET /api/profile
    Headers: Authorization: Bearer <token>
    """
    auth = JWTAuthentication()
    
    try:
        auth_result = auth.authenticate(request)
        if auth_result is None:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)

        user, token = auth_result
        user_profile = UserProfile.objects.get(user=user)

        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'profile': {
                'bio': user_profile.bio,
                'phone_number': user_profile.phone_number,
                'created_at': user_profile.created_at.isoformat(),
                'updated_at': user_profile.updated_at.isoformat(),
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@require_http_methods(["POST"])
def logout(request):
    """
    Logout user (client-side token removal recommended).
    
    POST /api/logout
    Headers: Authorization: Bearer <token>
    """
    auth = JWTAuthentication()
    
    try:
        auth_result = auth.authenticate(request)
        if auth_result is None:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return JsonResponse({
            'success': True,
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)


@csrf_exempt
@require_http_methods(["PUT", "POST"])
def update_profile(request):
    """
    Update user profile.
    
    PUT/POST /api/update-profile
    Headers: Authorization: Bearer <token>
    {
        "bio": "New bio",
        "phone_number": "+1234567890"
    }
    """
    auth = JWTAuthentication()
    
    try:
        auth_result = auth.authenticate(request)
        if auth_result is None:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)

        user, token = auth_result
        data = json.loads(request.body)
        
        user_profile = UserProfile.objects.get(user=user)
        
        if 'bio' in data:
            user_profile.bio = data['bio']
        if 'phone_number' in data:
            user_profile.phone_number = data['phone_number']
        
        user_profile.save()

        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully',
            'profile': {
                'bio': user_profile.bio,
                'phone_number': user_profile.phone_number,
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_401_UNAUTHORIZED)
