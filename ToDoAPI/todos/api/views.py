from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from todos.api.serializers import ToDoSerializer
from todos.models import ToDo
from core.pagination import StandardPagination


class ToDoAPIViewSet(viewsets.ModelViewSet):

    serializer_class = ToDoSerializer
    queryset = ToDo.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def list(self, request, *args, **kwargs):
        """
        Get a list of all ToDo.

        Returns a paginated list of ToDo objects.
        """
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single ToDo instance.

        Returns a single ToDo object.
        """
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new ToDo instance.

        Returns the newly created ToDo object.
        """
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Update an existing ToDo instance.

        This method updates an existing ToDo object with the provided data.
        """
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update an existing ToDo instance.

        This method updates an existing ToDo object with the provided data and
        only updates the fields specified in the request body.
        """
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing ToDo instance.

        This method deletes an existing ToDo object.
        """
        return super().destroy(request, *args, **kwargs)