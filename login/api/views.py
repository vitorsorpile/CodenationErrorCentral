from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from login.api.serializers import RegisterSerializer
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered a new user."
            data['username'] = user.username
            data['email'] = user.email
            data['token'] = Token.objects.get(user=user).key
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)    

        return Response(data, status=status.HTTP_201_CREATED)
