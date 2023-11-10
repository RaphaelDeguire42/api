from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import StateSerializer
from customModels.models import States


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
