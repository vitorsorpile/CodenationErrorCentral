from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from errors.models import Error
from errors.api.serializers import SimpleErrorSerializer, ErrorSerializer

@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def api_get_delete_archive_error_view(request, error_id):
    try:
        error = Error.objects.get(pk = error_id)
    except Error.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ErrorSerializer(error)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        if request.user != error.user:
            return Response({'Response': 'You don\'t permission to do this.'},
                            status= status.HTTP_401_UNAUTHORIZED)            

        operation = error.delete()
        if operation:
            return Response({'Success': 'Error Deleted'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'Failure': 'Delete Failed'},
                            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        
        error.archived = True
        error.save()

        if error.archived:
            return Response({'Success': 'Error Archived'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'Failure': 'Archive Failed'},
                            status=status.HTTP_400_BAD_REQUEST)


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


class ApiErrorListView(ListAPIView):
    serializer_class = SimpleErrorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        order_fields = ['level', 'date', '-date', '-events']
        search_fields = ['title', 'description', 'address'] 
        query_params = self.request.query_params
        
        queryset = Error.objects.filter(archived=False)

        if query_params:
            category = query_params.get('category', None)
            orderBy = query_params.get('orderBy', None)
            searchBy = query_params.get('searchBy', None)
            search = query_params.get('search', None)

            if category:
                queryset = queryset.filter(category=category)
            if searchBy in search_fields and search:
                query = searchBy + '__icontains'
                queryset = queryset.filter(**{query: search})
            if orderBy in order_fields:
                queryset = queryset.order_by(orderBy)
        
        return queryset


