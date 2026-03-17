from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from rolepermissions.decorators import has_role_decorator
from rolepermissions.roles import assign_role
from .roles import Trainee

from .serializer import UserCreateSerializer, UserViewSerializer

from .models import User

@has_role_decorator('trainer', 'admin')
@api_view(['POST'])
def create_trainee(request):
    serializer = UserCreateSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        assign_role(user, 'trainee')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@has_role_decorator('admin')
@api_view(['POST'])
def create_trainer(request):
    serializer = UserCreateSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        assign_role(user, 'trainer')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@has_role_decorator('trainer', 'admin')
@api_view(['GET'])
def view_users(request):
    trainee = User.objects.filter(groups='3') 
    serializer = UserViewSerializer(trainee, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@has_role_decorator('trainer', 'admin')
@api_view(['GET'])
def detail_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserViewSerializer(user)
    return Response(serializer.data)

@has_role_decorator('trainer', 'admin')
@api_view(['GET', 'DELETE'])
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserViewSerializer(user)
    user.delete()
    return Response(serializer.data)

@has_role_decorator('admin')
@api_view(['POST', 'GET'])
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserCreateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
