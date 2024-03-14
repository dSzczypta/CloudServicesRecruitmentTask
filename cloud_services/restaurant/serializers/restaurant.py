from rest_framework import serializers
from restaurant.models import Menu, Dish
import pytz
from cloud_services.settings import TIME_ZONE


class DateTimeWithTimeZone(serializers.DateTimeField):
    """
    A custom DateTimeField serializer that formats datetime with timezone.

    Attributes:
    - format (str): Date format string (default: "%Y-%m-%d %H:%M")
    """

    def to_representation(self, instance):
        """
        Convert datetime to string representation with timezone.

        Parameters:
        - instance (datetime): The datetime object to serialize.

        Returns:
        - str: String representation of datetime with timezone.
        """
        format = getattr(self, 'format', "%Y-%m-%d %H:%M")
        local_timezone = pytz.timezone(TIME_ZONE)
        return instance.astimezone(local_timezone).strftime(format) if instance else None

class DishSerializer(serializers.ModelSerializer):
    """
    Serializer for Dish model.

    Attributes:
    - created_dt (DateTimeWithTimeZone): Serializer for created_dt field.
    - updated_dt (DateTimeWithTimeZone): Serializer for updated_dt field.
    """
    created_dt = DateTimeWithTimeZone(required=False)
    updated_dt = DateTimeWithTimeZone(required=False)

    class Meta:
        """
        Meta class for DishSerializer.

        Attributes:
        - model (Menu): The Django model associated with the serializer.
        - fields (list): The fields to include in the serialized output.
        - read_only_fields (list): The fields that should be read-only.
        """
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'preparation_time',
                  'vegetarian', 'menu', 'created_dt', 'updated_dt']
        read_only_fields = ['created_dt', 'updated_dt']


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for Menu model.

    Attributes:
    - created_dt (DateTimeWithTimeZone): Serializer for created_dt field.
    - updated_dt (DateTimeWithTimeZone): Serializer for updated_dt field.
    - dishes (DishSerializer): Serializer for dishes field.
    """
    created_dt = DateTimeWithTimeZone(required=False)
    updated_dt = DateTimeWithTimeZone(required=False)
    dishes = DishSerializer(many=True, required=False)

    class Meta:
        """
        Meta class for MenuSerializer.

        Attributes:
        - model (Menu): The Django model associated with the serializer.
        - fields (list): The fields to include in the serialized output.
        - read_only_fields (list): The fields that should be read-only.
        """
        model = Menu
        fields = ['id', 'name', 'description',
                  'created_dt', 'updated_dt', 'dishes']
        read_only_fields = ['created_dt', 'updated_dt', 'dishes']
