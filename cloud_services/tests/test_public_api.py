from datetime import datetime, timedelta

import pytest
import requests
from django.contrib.auth.models import User
from django.test import Client
from django.utils import timezone
# models
from restaurant.models import Dish, Menu


@pytest.fixture
def client():
    client = Client()
    yield client


@pytest.fixture
def menu():
    menu_data = {
        "name": "test_menu",
        "description": "test menu description",
        "created_dt": "2024-03-14 08:00",
        "updated_dt": "2024-03-15 08:00",
    }
    menu = Menu.objects.create(**menu_data)
    return menu


@pytest.fixture
def dish(menu):
    dish_data = {
        "name": "test_dish",
        "menu": menu,
        "description": "test dish description",
        "price": 20.20,
        "preparation_time": "00:00:30",
        "vegetarian": False,
        "created_dt": datetime(2023, 3, 12, 9, 15),
        "updated_dt": datetime(2023, 4, 12, 9, 15),
    }

    dish = Dish.objects.create(**dish_data)
    return dish


@pytest.mark.django_db
def test_empty_public_api(client):
    url = "/api/public/menu"
    response = client.get(url)
    assert isinstance(response.data, list)
    assert len(response.data) == 0


@pytest.mark.django_db
def test_populated_public_api(client, dish):
    url = "/api/public/menu"
    response = client.get(url)
    assert isinstance(response.data, list)
    assert len(response.data) == 1


@pytest.mark.django_db
def test_public_api_filter(client, dish):
    menu = dish.menu
    my_delta = timedelta(hours=5)

    filters = [
        f"name={menu.name}",
        f"start_created_dt={datetime.strftime(menu.created_dt - my_delta , format='%Y-%m-%d %H:%M')}",
        f"end_created_dt={datetime.strftime(menu.created_dt + my_delta, format='%Y-%m-%d %H:%M')}",
        f"start_udpated_dt={datetime.strftime(menu.updated_dt - my_delta, format='%Y-%m-%d %H:%M')}",
        f"end_udpated_dt={datetime.strftime(menu.updated_dt + my_delta, format='%Y-%m-%d %H:%M')}",
    ]
    filter_params_str = "&".join(filters)
    url = f"/api/public/menu?{filter_params_str}"


    response = client.get(url)
    assert isinstance(response.data, list)
    assert len(response.data) == 1