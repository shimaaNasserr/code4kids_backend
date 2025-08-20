from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import re
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect



@api_view(['POST'])
def register(request):
    data = request.data

    required_fields = ['username', 'email', 'password', 'confirm_password', 'role']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return Response({"error": f"{field} is required."}, status=400)

    if data['role'].lower() == 'admin':
        return Response({"error": "You are not allowed to register as an Admin."}, status=403)
        
    if data['password'] != data['confirm_password']:
        return Response({"error": "Passwords do not match."}, status=400)

    if data['role'] not in ['Kid', 'Parent']:
        return Response({"error": "Role must be either 'Kid' or 'Parent'."}, status=400)

    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()

        if user.role == 'Admin':
            user.is_staff = True
            user.is_superuser = True
            user.save()

        return Response({ 
            "message": "User Registered", 
            "user": UserSerializer(user).data 
        }, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def loginUser(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            },
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, status=200)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def parent_only_view(request):
    if request.user.role != 'Parent':
        return Response({"error": "Access denied. Parent role required."}, status=403)

    return Response({"message": f"Hello {request.user.first_name}, welcome to the Parent Dashboard!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kid_only_view(request):
    if request.user.role != 'Kid':
        return Response({"error": "Access denied. Kid role required."}, status=403)

    return Response({"message": f"Hello {request.user.first_name}, welcome to the Kid Zone!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_only_view(request):
    if request.user.role != 'Admin':
        return Response({"error": "Access denied. Admin role required."}, status=403)

    return Response({"message": f"Welcome Admin {request.user.first_name} to the Admin Panel!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)



def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def google_login_redirect(request):
    user = request.user  # ده بيكون المستخدم اللي اتسجل بجوجل
    
    if not user.is_authenticated:
        return redirect("http://localhost:5173/")  # لو فشل الدخول

    # نولّد JWT tokens
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    # نجهز redirect على الـ frontend مع التوكنز
    frontend_url = f"http://localhost:5173/?access={access}&refresh={str(refresh)}"
    return redirect(frontend_url)

