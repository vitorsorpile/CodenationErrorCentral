from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from login.models import User
from errors.models import Error
from errors.api.serializers import UserSerializer, ErrorSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_detail_error_view(request, error_id):
    try:
        error = Error.objects.get(pk=error_id)
    except Error.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # user = request.user
    # if error.user != user:
    #     return Response({'Response': 'You don\'t permission to access this page.'},
    #                     status= status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        serializer = ErrorSerializer(error)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_archive_error_view(request, error_id):
    try:
        error = Error.objects.get(pk=error_id)
    except Error.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if error.user != user:
        return Response({'Response': 'You don\'t permission to access this page.'},
                        status= status.HTTP_401_UNAUTHORIZED)

    if request.method == "POST":
        error.archived = True
        error.save()

        if error.archived:
            return Response({'Success': 'Error archived'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'Failure': 'Archive failed'},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_error_view(request, error_id):
    try:
        error = Error.objects.get(pk=error_id)
    except Error.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if error.user != user:
        return Response({'Response': 'You don\'t permission to access this page.'},
                        status= status.HTTP_401_UNAUTHORIZED)
    
    if request.method == "DELETE":
        operation = error.delete()
        data = {}
        if operation:
            data['success'] = 'Error deleted'
        else:
            data['failure'] = 'Delete failed'
        return Response(data=data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_error_view(request): 
    user = request.user
    
    error = Error()
    error.user = user

    if request.method == "POST":
        serializer = ErrorSerializer(error, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def api_update_error_view(request, error_id):
    try:
        error = Error.objects.get(pk=error_id)
    except Error.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if error.user != user:
        return Response({'Response': 'You don\'t permission to access this page.'},
                        status= status.HTTP_401_UNAUTHORIZED)

    if request.method == "PUT":
        serializer = ErrorSerializer(error, data=request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['success'] = "Error updated"
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)