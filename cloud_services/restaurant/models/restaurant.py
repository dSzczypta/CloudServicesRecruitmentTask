from django.db import models
from rest_framework.exceptions import ValidationError
from cloud_services.settings import MAX_UPLOAD_SIZE


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)


class Dish(models.Model):
    name = models.CharField(max_length=255)
    menu = models.ForeignKey(
        Menu, related_name='dishes', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    preparation_time = models.DurationField()
    vegetarian = models.BooleanField(default=False)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'menu')


def file_size_validator(value):
    if value.size > MAX_UPLOAD_SIZE:
        raise ValidationError(
            'File too large. Size should not exceed {0} bytes.'.format(MAX_UPLOAD_SIZE))


class DishAttachment(models.Model):
    file = models.FileField(upload_to='uploads/dish/%Y/%m/%d/', validators=[file_size_validator], max_length=250)
    dish = models.ForeignKey('restaurant.Dish', related_name='files', on_delete=models.CASCADE)
