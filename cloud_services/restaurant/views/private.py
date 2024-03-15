from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser

from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.db import IntegrityError

from drf_yasg.utils import swagger_auto_schema

from restaurant.models import Menu, Dish, DishAttachment
from restaurant.serializers import MenuSerializer, DishSerializer, DishAttachmentSerializer


class MenuGenericAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    A generic API view for handling menu items.

    List, retrieve, create, update, and delete menu items.

    Parameters:
    - pk: ID of the menu item (optional)    

    GET: 
    - Retrieve a list of all menu items or retrieve a specific menu item by its ID.

    POST: 
    - Create a new menu item.

    PATCH: 
    - Update a specific menu item partially.

    DELETE: 
    - Delete a specific menu item.
    """

    queryset = Menu.objects
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{'Bearer': []}]
    )
    def get(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a list of all menu items or retrieve a specific menu item by its ID.

        Parameters:
        - pk: ID of the menu item (optional)

        Returns:
        - Returns a list of all menu items or details of the specified menu item.
        """
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })
        return self.list(request)

    def post(self, request, *args, **kwargs):
        """
        Create a new menu item.

        Request Body:
        - Menu item data in JSON format.

        Returns:
        - Returns the newly created menu item data.
        """
        return Response({
            'data': self.create(request).data
        })

    def patch(self, request, pk, *args, **kwargs):
        """
        Update a specific menu item partially.

        Parameters:
        - pk: ID of the menu item

        Request Body:
        - Partial data to update.

        Returns:
        - Returns the updated menu item data.
        """
        return Response({
            'data': self.update(request, pk, partial=True).data
        })

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete a specific menu item.

        Parameters:
        - pk: ID of the menu item

        Returns:
        - Returns no content if the menu item is successfully deleted.
        """
        try:
            self.queryset.filter(id=pk).delete()

        except (ProtectedError, IntegrityError) as e:
            return Response({"message": f'You cannot delete a {self.queryset.model.__name__}. It is linked to other resources', "details": getattr(e, 'message', str(e))}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DishGenericAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    A generic API view for handling dishes.

    List, retrieve, create, update, and delete dishes.

    Parameters:
    - pk: ID of the dish (optional)    

    GET: 
    - Retrieve a list of all dishes or retrieve a specific dish by its ID.

    POST: 
    - Create a new dish.

    PATCH: 
    - Update a specific dish partially.

    DELETE: 
    - Delete a specific dish.
    """
    queryset = Dish.objects
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a list of all dishes or retrieve a specific dish by its ID.

        Parameters:
        - pk: ID of the dish (optional)

        Returns:
        - Returns a list of all dishes or details of the specified dish.
        """
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })
        return self.list(request)

    def post(self, request, *args, **kwargs):
        """
        Create a new dish.

        Request Body:
        - Dish data in JSON format.

        Returns:
        - Returns the newly created dish data.
        """
        return Response({
            'data': self.create(request).data
        })

    def patch(self, request, pk, *args, **kwargs):
        """
        Update a specific dish partially.

        Parameters:
        - pk: ID of the dish

        Request Body:
        - Partial data to update.

        Returns:
        - Returns the updated dish data.
        """
        return Response({
            'data': self.update(request, pk, partial=True).data
        })

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete a specific dish.

        Parameters:
        - pk: ID of the dish

        Returns:
        - Returns no content if the dish is successfully deleted.
        """
        try:
            self.queryset.filter(id=pk).delete()

        except (ProtectedError, IntegrityError) as e:
            return Response({"message": f'You cannot delete a {self.queryset.model.__name__}. It is linked to other resources', "details": getattr(e, 'message', str(e))}, status=status.HTTP_409_CONFLICT)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DishAttachmentGenericAPI(generics.GenericAPIView, mixins.CreateModelMixin,):
    """
    A class-based view for handling DishAttachment creation via API.

    Attributes:
        permission_classes (list): A list containing the permission classes required for accessing the view.
        queryset (QuerySet): The queryset containing DishAttachment objects.
        serializer_class (Serializer): The serializer class responsible for serializing DishAttachment objects.
        parser_classes (list): A list containing the parser classes used for parsing incoming request data.

    Methods:
        post(request, format=None):
            Handles POST requests to create DishAttachment objects.
            Args:
                request (HttpRequest): The HTTP request object containing the data.
                format (str, optional): The format of the response. Defaults to None.
            Returns:
                Response: An HTTP response indicating the result of the operation.

    Example:
        To create a DishAttachment object via API, send a POST request with the required data.
    """
    permission_classes = [IsAuthenticated]
    queryset = DishAttachment.objects
    serializer_class = DishAttachmentSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        """
        Handles POST requests to create DishAttachment objects.

        Args:
            request (HttpRequest): The HTTP request object containing the data.
            format (str, optional): The format of the response. Defaults to None.

        Returns:
            Response: An HTTP response indicating the result of the operation.
        """
        if 'files' in request.data:
            files = request.data.pop('files')
            for file in files:
                data = {"dish_id": request.data["id"], "file": file}
                try:
                    att = DishAttachment(**data)
                    att.save()
                except ValidationError as e:
                    return Response(e.message_dict, status.HTTP_400_BAD_REQUEST)

        return Response({"message": "success"}, status.HTTP_201_CREATED)
