from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import ProjectSerializer, ProjectDetailsSerializer
from customModels.models import Classes, Project, States
import os
import shutil


######## PROJETS ##################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_details(request, pk):
    project = Project.objects.get(id=pk)
    classes = Classes.objects.filter(project=project)
    states = States.objects.filter(project=project)
    serializer = ProjectDetailsSerializer(project, context={'classes': classes, 'states': states})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_related_projects(request):
    user = request.user
    related_projects = user.projects.all()

    serializer = ProjectSerializer(related_projects, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_create(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save()

        user = request.user

        user.projects.add(project)

        limit_projects(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def limit_projects(user):

    max_projects_to_keep = 10

    user_email = user.email
    parts = user_email.split('@')
    user_name = parts[0]
    unique_user_name = user_name + "_" + str(user.id)
    testing = os.path.dirname(os.path.abspath(__file__))
    repo_dir = os.path.dirname(os.path.dirname(testing))
    print(os.path.join(repo_dir, 'memory', f'{unique_user_name}'))
    if os.path.join(repo_dir, 'memory', f'{unique_user_name}'):
        user_projects_dir = os.path.join(repo_dir, 'memory', f'{unique_user_name}')
        if not os.path.exists(user_projects_dir):
            os.makedirs(user_projects_dir)
        all_projects = os.listdir(user_projects_dir)
        all_projects.sort(key=lambda x: os.path.getctime(os.path.join(user_projects_dir, x)))
        projects_to_delete = max(0, len(all_projects) - max_projects_to_keep)

        for project_name in all_projects[:projects_to_delete]:
            project_path = os.path.join(user_projects_dir, project_name)
            shutil.rmtree(project_path)

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

