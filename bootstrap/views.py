from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import json
import cv2
import glob
import os
from django.shortcuts import render
from rest_framework.response import Response
from django.http import JsonResponse




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
def upload(request):
    User = get_user_model()
    file_name = request.data.get('file_name')
    user_id = request.data.get('user_id')
    json_data = request.data.get('json')

    api_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    memory_folder = os.path.join(api_root, 'memory')
    if '.' in file_name:
        file_name = os.path.splitext(file_name)[0]


    if file_name is not None and user_id is not None and json_data is not None:
        user_id = int(user_id)
        user = User.objects.filter(id=user_id).first()
        user_name = user.email.split('@')[0]
        json_path = os.path.join(memory_folder, user_name, file_name)
        json_file = os.path.join(memory_folder, user_name, file_name, file_name + '.json')

        if not os.path.exists(json_path):
            os.makedirs(json_path)
        
        if os.path.exists(json_file):
            with open(json_file, 'r') as file:
                existing_data = json.load(file)

            existing_data.update(json_data)

            with open(json_file, 'w') as file:
                json.dump(existing_data, file)

        else:
            with open(json_file, 'w') as file:
                json.dump(json_data, file)

        return Response('JSON data written to file.')
    
    else:
        return Response("There's a missing parameter in the request")
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def voir_json(request):
    start = int(request.GET.get('start', 0))
    end = int(request.GET.get('end', 10))

    json_file = open('json/last_run_data.json')
    data_dict = json.load(json_file)
   

    result_data = []

    for data in data_dict[start:end]:
        mice = data.get("mouse", {})
        for number in mice:
            mouse = mice[number]
            result_data.append({"mouse": mouse})

        obstacles = data.get("lit", {})
        for number in obstacles:
            bed = obstacles[number]
            result_data.append({"bed": bed})

        obstacles = data.get("mangeoire", {})
        for number in obstacles:
            eatingStation = obstacles[number]
            result_data.append({"eatingStation": eatingStation})

        obstacles = data.get("eau", {})
        for number in obstacles:
            waterStation = obstacles[number]
            result_data.append({"waterStation": waterStation})

        obstacles = data.get("roulette", {})
        for number in obstacles:
            wheel = obstacles[number]
            result_data.append({"wheel": wheel})
    json_file.close()
    return JsonResponse(result_data, safe=False)
