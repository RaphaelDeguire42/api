from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializer import UserSerializer, ProjectDetailsSerializer, ProjectSerializer, ClassSerializer, StateSerializer
from customModels.models import Project, Classes, States
from django.db import IntegrityError
import jwt





############### USERS #####################

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


######## PROJETS ##################


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_related_projects(request):
    user = request.user
    related_projects = user.projects.all()

    serializer = ProjectSerializer(related_projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_details(request, pk):
    project = Project.objects.get(id=pk)
    classes = Classes.objects.filter(project=project)
    states = States.objects.filter(project=project)
    serializer = ProjectDetailsSerializer(project, context={'classes': classes, 'states': states})
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_create(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save()

        user = request.user

        user.projects.add(project)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def project_update(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(project, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def project_delete(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


#### CLASSES ##############

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def classes_details(request, pk):
    classes = Classes.objects.get(id=pk)
    serializer = ClassSerializer(classes)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def classes_create(request):
    serializer = ClassSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def classes_update(request, pk):
    try:
        classes = Classes.objects.get(id=pk)
    except Classes.DoesNotExist:
        return Response({"detail": "Classes not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClassSerializer(classes, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def classes_delete(request, pk):
    try:
        classes = Classes.objects.get(id=pk)
    except Classes.DoesNotExist:
        return Response({"detail": "Classes not found."}, status=status.HTTP_404_NOT_FOUND)

    classes.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


############### STATES ################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def states_details(request, pk):
    states = States.objects.get(id=pk)
    serializer = StateSerializer(states)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def states_create(request):
    serializer = StateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def states_update(request, pk):
    try:
        states = States.objects.get(id=pk)
    except States.DoesNotExist:
        return Response({"detail": "States not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = StateSerializer(states, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def states_delete(request, pk):
    try:
        states = States.objects.get(id=pk)
    except States.DoesNotExist:
        return Response({"detail": "States not found."}, status=status.HTTP_404_NOT_FOUND)

    states.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
