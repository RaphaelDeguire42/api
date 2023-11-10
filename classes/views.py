from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import ClassSerializer
from customModels.models import Classes


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
