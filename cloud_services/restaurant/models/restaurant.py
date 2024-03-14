from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)


class Dish(models.Model):
    name = models.CharField(max_length=255)
    menu = models.ForeignKey(Menu, related_name='dishes', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    preparation_time = models.DurationField() 
    vegetarian = models.BooleanField(default=False)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'menu')
        