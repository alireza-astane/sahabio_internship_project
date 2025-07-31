"""
Serializers for App model.

This module defines the AppSerializer class, which serializes and deserializes App model instances
for use with Django REST Framework.

Classes:
    AppSerializer: Serializes all fields of the App model.

Swagger Documentation:
    The AppSerializer exposes all fields of the App model for API input and output.
    Use this serializer in your API views to automatically generate Swagger/OpenAPI documentation
    for the App endpoints, including all model fields.
"""

from rest_framework import serializers
from .models import App


class AppSerializer(serializers.ModelSerializer):
    """
    AppSerializer

    Serializer for the App model, providing automatic field generation for all model fields.

    This serializer is used to convert App model instances to and from JSON representations,
    enabling easy integration with Django REST Framework APIs.

    Swagger Documentation:
    - Serializes all fields of the App model.
    - Used for input and output in API endpoints related to App objects.

    Attributes:
        Meta.model (App): The model associated with this serializer.
        Meta.fields (str): Specifies that all fields of the model are included.

    Usage Example:
        Used in API views to serialize/deserialize App instances.

    """

    class Meta:
        """
        Meta class for the App serializer.
        Attributes:
            model (App): Specifies the model to be serialized.
            fields (str): Indicates that all fields of the model should be included.
        Swagger Documentation:
            This Meta configuration ensures that all fields of the App model are exposed in the API schema.
            When using drf-yasg or drf-spectacular, all model fields will be automatically documented in the generated Swagger/OpenAPI specification.
        """

        model = App
        fields = "__all__"
