from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rolepermissions.roles import assign_role
from .roles import Trainee

from .serializer import UserCreateSerializer, UserViewSerializer

from .models import User

@api_view(['POST'])
def CreateUser(request):
    serializer = UserCreateSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        assign_role(user, 'trainee')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ViewUser(request):
    serializer = UserViewSerializer(User.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def DetailUser(request, pk):
    user = User.objects.get(pk = pk)
    serializer = UserViewSerializer(user)
    if user:
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'DELETE'])
def DeleteUser(request, pk):
    user = User.objects.get(pk = pk)
    serializer = UserViewSerializer(user)
    user.delete()
    return Response(serializer.data)

@api_view(['POST'])
def UpdateUser(request, pk):
    user = User.objects.get(pk = pk)
    serializer = UserCreateSerializer(user)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    
