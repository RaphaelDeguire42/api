from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
import json
import os
import io
import cv2
import base64
import numpy as np
from django.shortcuts import render
from rest_framework.response import Response
from django.http import FileResponse, JsonResponse
from customModels.models import ProjectConfig, Project, FeedbackLog




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
    User         = get_user_model()
    user_id      = request.user.id
    file_name    = request.data.get('fileName')
    json_data    = request.data.get('json')
    video_name   = request.data.get('videoName')
    project_name = request.data.get('projectName')
    frame_number = "frame" + json.dumps(request.data.get('frameNumber'))

    api_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    memory_folder = os.path.join(api_root, 'memory')

    # If all required parameters are present
    if file_name is not None and user_id is not None and json_data is not None and frame_number is not None:
        user_id = int(user_id)
        user = User.objects.filter(id=user_id).first()
        user_email = user.email
        parts = user_email.split('@')
        user_name = parts[0]
        unique_user_name = user_name + "_" + str(user_id)
        
        try:
            # si le user existe on crée un folder spécifique
            if user is not None:
                file_name, file_extension = os.path.splitext(file_name)
                user_folder = os.path.join(memory_folder, unique_user_name)
                project_folder = os.path.join(user_folder, project_name)
                video_folder = os.path.join(project_folder, video_name)
                json_folder = os.path.join(video_folder, 'json')

                # on cré le folder si il existe pas
                if not os.path.exists(json_folder):
                    os.makedirs(json_folder)

                # on construit le path avec le file number
                frame_filename = os.path.join(json_folder, f'{video_name}_{frame_number}.json')

                try:
                    # Parse le json qu'on recoit
                    parsed_json_data = json.loads(json_data)
                except json.JSONDecodeError as e:
                    return Response(f'Invalid JSON data: {str(e)}', status=400)

                # ca existe tu?
                if os.path.exists(frame_filename):
                    # on lis le json avec le load
                    with open(frame_filename, 'r') as file:
                        existing_data = json.load(file)

                    # les json est tu différent?
                    if parsed_json_data != existing_data:
                        # si oui on overwrite
                        with open(frame_filename, 'w') as file:
                            json.dump(parsed_json_data, file, indent=2)
                        print(f"No Changes | Username: {user_name} | Project: {project_name} |  Video: {video_name}  | Frame: {frame_number}")
                        return Response('JSON update')  # on update
                    else:
                        print(f"Changes Made | Username: {user_name} | Project: {project_name} |  Video: {video_name}  | Frame: {frame_number}")
                        return Response('JSON non-change')  # on change rien
                else:
                    # si le fichier existe pas on crée le fichier
                    with open(frame_filename, 'w') as file:
                        json.dump(parsed_json_data, file, indent=2)
                    return Response('Fichier JSON creer')  # on le crée
        except Exception as e:
            print(e)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    User            = get_user_model()
    user_id         = request.user.id
    encoded_image   = request.data.get('image')
    file_name       = request.data.get('file_name')
    video_name      = request.data.get('video_name')
    project_name = request.data.get('project_name')
    frame_number = "frame" + json.dumps(request.data.get('frame_number'))
    print(user_id)
    print(file_name)
    print(video_name)
    print(project_name)
    print(frame_number)

    if encoded_image:
        decoded_image = base64.b64decode(encoded_image)

        image_stream = io.BytesIO(decoded_image)
        image_stream.seek(0)

        img = cv2.imdecode(np.frombuffer(image_stream.read(), np.uint8), cv2.IMREAD_COLOR)

        api_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        memory_folder = os.path.join(api_root, 'memory')

        user_id = int(user_id)
        user = User.objects.filter(id=user_id).first()
        user_email = user.email
        parts = user_email.split('@')
        user_name = parts[0]
        unique_user_name = user_name + "_" + str(user_id)

        if user is not None:
            file_name, file_extension = os.path.splitext(file_name)
            user_folder = os.path.join(memory_folder, unique_user_name)
            project_folder = os.path.join(user_folder, project_name)
            video_folder = os.path.join(project_folder, video_name)
            frames_folder = os.path.join(video_folder, 'frames')

            if not os.path.exists(frames_folder):
                os.makedirs(frames_folder)

            frame_filename = os.path.join(frames_folder, f'{frame_number}.webp')
            if not os.path.exists(frame_filename):
                cv2.imwrite(frame_filename, img)

            return JsonResponse({'message': 'Image saved successfully.'})
    
    return JsonResponse({"error": "There's a missing parameter in the request"}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feedback_log_list(request):
    feedback_logs = FeedbackLog.objects.all()
    data = [{"id": log.id, "user_id": log.user_id, "feedback": log.feedback} for log in feedback_logs]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def feedback_log_create(request):
    if 'feedback' not in request.data:
        return Response({"Message": "Please provide a 'feedback' field"}, status=status.HTTP_400_BAD_REQUEST)

    feedback_log = FeedbackLog.objects.create(user_id=request.user.id, feedback=request.data['feedback'])
    data = {"id": feedback_log.id, "user_id": feedback_log.user_id, "feedback": feedback_log.feedback}
    return Response(data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def feedback_log_destroy():
    FeedbackLog.objects.all().delete()
    data = {"message": "All feedback logs have been deleted"}
    return Response(data, status=status.HTTP_200_OK)