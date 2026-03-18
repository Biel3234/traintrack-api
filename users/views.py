from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .roles import IsTrainer, IsAdmin

from .serializer import UserCreateSerializer, UserViewSerializer

from .models import User

from .filters import UserFilter

@permission_classes([IsTrainer, IsAdmin])
@api_view(['POST'])
def create_trainee(request):
    data = request.data.copy()
    data['role'] = 'trainee'
    serializer = UserCreateSerializer(data = data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsTrainer, IsAdmin])
@api_view(['POST'])
def create_trainer(request):
    data = request.data.copy()
    data['role'] = 'trainer'
    serializer = UserCreateSerializer(data = data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsTrainer, IsAdmin])
@api_view(['GET'])
def view_users(request):
    queryset = User.objects.all()
    filter = UserFilter(request.GET, queryset=queryset)

    if not filter.is_valid():
        return Response(filter.errors, status=400)

    serializer = UserViewSerializer(filter.qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsTrainer, IsAdmin])
@api_view(['GET'])
def detail_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserViewSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsAdmin])
@api_view(['GET', 'DELETE'])
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserViewSerializer(user)
    user.delete()
    return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsAdmin])
@api_view(['POST', 'GET'])
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserCreateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
