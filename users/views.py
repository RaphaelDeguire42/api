from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializer import UserSerializer, ProjectSerializer
from customModels.models import Project, Classes, States
from django.db import IntegrityError
import jwt
from customModels.models import ProjectConfig, Project






############### USERS #####################



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_related_projects(request):
    user = request.user
    related_projects = user.projects.all()

    serializer = ProjectSerializer(related_projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request, pk):
    User = get_user_model()
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)



@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            error_message = {'message': 'This email address is already taken'}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    User = get_user_model()
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    User = get_user_model()
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_authentication(request):
    token = request.META.get('HTTP_AUTHORIZATION').split()[1]

    decoded_token = jwt.decode(token, options={"verify_signature": False})
    user_id = decoded_token.get('user_id')

    return Response({"status": "yes", "user_id": user_id})
