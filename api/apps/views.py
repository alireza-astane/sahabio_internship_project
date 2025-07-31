"""
AppViewSet handles CRUD operations for the App model.

This viewset provides endpoints to list, retrieve, create, update, and delete App instances.

Swagger Documentation:
    - list: Retrieve a list of all apps.
    - retrieve: Get details of a specific app by ID.
    - create: Add a new app.
    - update: Update an existing app.
    - partial_update: Partially update an app.
    - destroy: Delete an app.

Attributes:
    queryset (QuerySet): All App objects from the database.
    serializer_class (Serializer): Serializer class for App model.

Usage:
    Register this viewset with a router in your urls.py to expose the API endpoints.
"""

from rest_framework import viewsets
from .models import App
from .serializers import AppSerializer


class AppViewSet(viewsets.ModelViewSet):
    """
    AppViewSet is a ModelViewSet for managing App instances.
    Provides CRUD operations for App model.
    Swagger Documentation:
        - list: Retrieve a list of all apps.
        - retrieve: Get details of a specific app by ID.
        - create: Add a new app.
        - update: Update an existing app.
        - partial_update: Partially update an app.
        - destroy: Delete an app.
    Attributes:
        queryset (QuerySet): Queryset of all App objects.
        serializer_class (Serializer): Serializer class for App model.
    """

    queryset = App.objects.all()
    serializer_class = AppSerializer
