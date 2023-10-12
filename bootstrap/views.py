from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import json
import os
from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse, FileResponse
from customModels.models import ProjectConfig, Project



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ajout_dossier(request):
    User = get_user_model()
    path = str(request.data.get('path'))
    user_id = request.data.get('user_id')

    response_data = {
        'path': path,
        'user_id': user_id
    }

    if user_id is not None:
        user_id = int(user_id)
        user = User.objects.filter(id=user_id).first()
        if user is not None:
            user.workplace = path
            user.save()

    return JsonResponse(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload(request):
    User = get_user_model()
    file_name = request.data.get('file_name')
    user_id = request.user.id
    json_data = request.data.get('json')

    api_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    memory_folder = os.path.join(api_root, 'memory')
    
    if file_name is not None and user_id is not None and json_data is not None:
        user_id = int(user_id)
        user = User.objects.filter(id=user_id).first()

        if user is not None:
            file_name, file_extension = os.path.splitext(file_name)

            user_folder = os.path.join(memory_folder, str(user_id))
            json_file = os.path.join(user_folder, f'{file_name}.json')

            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            if os.path.exists(json_file):
                with open(json_file, 'r') as file:
                    existing_data = json.load(file)

                if existing_data != json_data:
                    with open(json_file, 'w') as file:
                        json.dump(json_data, file)
                    return Response('JSON data updated.')

            else:
                with open(json_file, 'w') as file:
                    json.dump(json_data, file)

            return Response('JSON data written to file.')

    return Response("There's a missing parameter in the request")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def store_config(request):
    project_id = request.data.get('project_id')
    duree = request.data.get('duree')
    sequence = request.data.get('sequence')

    if not (project_id and duree and sequence):
        return Response({'error': 'Ce endpoint a besoin du id du projet, de la durée et du temps des séquences'}, status=400)

    try:
        project_id = int(project_id)
        duree = float(duree)
        sequence = float(sequence)
    except (ValueError, TypeError):
        return Response({'error': 'le type de data accepté est en INT ou en Float'}, status=400)

    try:
        project_config = ProjectConfig.objects.get(project_id=project_id)
        project_config.duree = duree
        project_config.sequence = sequence
        project_config.save()
    except ProjectConfig.DoesNotExist:
        project_config = ProjectConfig(project_id=project_id, duree=duree, sequence=sequence)
        project_config.save()

    response_data = {
        'project_id': project_id,
        'duree': duree,
        'sequence': sequence
    }

    return Response(response_data, status=201)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_json(request):
    User = get_user_model()
    user_id = request.user.id  
    project_id = request.data.get('project_id') 

    
    if not project_id:
        return Response({"error": "project_id is required in query parameters"}, status=400)

    user_folder = os.path.join('memory', str(user_id))
    try:
        project = Project.objects.get(id=project_id)
        folder_name = project.folderName
        json_file_path = os.path.join(user_folder, f'{folder_name}.json')

        if os.path.exists(json_file_path):
            response = FileResponse(open(json_file_path, 'rb'))
            response['Content-Type'] = 'application/json'
            response['Content-Disposition'] = f'attachment; filename="{folder_name}.json"'
            return response
        else:
            return Response({"error": "JSON file not found"}, status=404)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)

 