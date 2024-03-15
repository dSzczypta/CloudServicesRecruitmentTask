from django.core.files.uploadedfile import SimpleUploadedFile
import pytest

# models
from restaurant.models import Menu, Dish, DishAttachment
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def superuser_client():
    username = 'admin'
    password = 'admin_password'
    email = 'admin@example.com'
    User.objects.create_superuser(username, email, password)

    client = Client()
    client.login(username=username, password=password)

    url = '/api/token/'
    response = client.post(url, {"username": username, "password": password})

    token = f'Bearer {response.data["access"]}'
    client.defaults['HTTP_AUTHORIZATION'] = token
    yield client

    User.objects.filter(username=username).delete()


@pytest.fixture
def menu():
    data = {
        "name": "Menu Mexican",
        "description": "Savory Mexican Flavors",
        "created_dt": "2024-03-14T08:00:00Z",
        "updated_dt": "2024-03-14T08:00:00Z"
    }
    obj = Menu.objects.create(**data)
    return obj


@pytest.mark.django_db
def test_get_list_menu(superuser_client, menu):
    response = superuser_client.get('/api/private/menu')
    assert response.status_code == 200

    data = response.data
    assert len(data) > 0
    assert isinstance(data, list)


@pytest.mark.django_db
def test_retrive_menu(superuser_client, menu):
    response = superuser_client.get(f'/api/private/menu/{menu.id}')
    assert response.status_code == 200
    data = response.data['data']

    assert data['id'] == menu.id
    assert data['name'] == menu.name
    assert data['description'] == menu.description


@pytest.mark.django_db
def test_create_menu(superuser_client):
    data = {
        "name": "Menu Italian",
        "description": "Delicious Italian Cuisine",
        "created_dt": "2024-03-14 08:00",
        "updated_dt": "2024-03-14 08:00"
    }

    response = superuser_client.post(
        '/api/private/menu', data, content_type="application/json")
    assert response.status_code == 200

    item = response.data['data']
    assert Menu.objects.count() == 1
    assert item['name'] == data['name']
    assert item['description'] == data['description']


@pytest.mark.django_db
def test_edit_menu(superuser_client, menu):
    data = {'name': 'test1'}
    response = superuser_client.patch(
        f'/api/private/menu/{menu.id}', data=data, content_type="application/json")

    data = response.data['data']
    assert response.status_code == 200
    assert data['id'] == menu.id
    assert data['name'] == data['name']
    assert data['description'] == menu.description


@pytest.mark.django_db
def test_edit_incorect_menu(superuser_client, menu):
    data = {'created_dt': 'test1'}
    response = superuser_client.patch(
        f'/api/private/menu/{menu.id}', data=data, content_type="application/json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_menu(superuser_client, menu):
    response = superuser_client.delete(
        f'/api/private/menu/{menu.id}', content_type="application/json")

    assert response.status_code == 204
    assert not Menu.objects.all().exists()


@pytest.fixture
def dish(menu):
    data = {
        "name": "Pizza Margherita",
        "menu_id": menu.id,
        "description": "Classic pizza topped with tomato sauce, mozzarella cheese, and fresh basil leaves.",
        "price": "10.00",
        "preparation_time": "00:25:00",
        "vegetarian": True,
        "created_dt": "2024-03-14T08:00:00Z",
        "updated_dt": "2024-03-14T08:00:00Z"
    }
    obj = Dish.objects.create(**data)
    return obj


@pytest.mark.django_db
def test_get_list_dish(superuser_client, dish):
    response = superuser_client.get('/api/private/dish')
    assert response.status_code == 200

    data = response.data
    assert len(data) > 0
    assert isinstance(data, list)


@pytest.mark.django_db
def test_retrive_dish(superuser_client, dish):
    response = superuser_client.get(f'/api/private/dish/{dish.id}')
    assert response.status_code == 200
    data = response.data['data']

    assert data['id'] == dish.id
    assert data['name'] == dish.name
    assert data['description'] == dish.description
    assert data['vegetarian'] == dish.vegetarian


@pytest.mark.django_db
def test_create_dish(superuser_client, menu):
    data = {
        "name": "Pizza Margherita",
        "menu": menu.id,
        "description": "Classic pizza topped with tomato sauce, mozzarella cheese, and fresh basil leaves.",
        "price": "10.00",
        "preparation_time": "00:25:00",
        "vegetarian": True,
        "created_dt": "2024-03-14 08:00:00",
        "updated_dt": "2024-03-14 08:00:00"
    }

    response = superuser_client.post(
        '/api/private/dish', data, content_type="application/json")
    assert response.status_code == 200

    item = response.data['data']
    assert Dish.objects.count() == 1
    assert item['name'] == data['name']
    assert item['description'] == data['description']
    assert item['vegetarian'] == data['vegetarian']


@pytest.mark.django_db
def test_edit_dish(superuser_client, dish):
    data = {'name': 'test1'}
    response = superuser_client.patch(
        f'/api/private/dish/{dish.id}', data=data, content_type="application/json")

    data = response.data['data']
    assert response.status_code == 200
    assert data['id'] == dish.id
    assert data['name'] == data['name']
    assert data['description'] == dish.description
    assert data['vegetarian'] == dish.vegetarian


@pytest.mark.django_db
def test_edit_incorect_dish(superuser_client, dish):
    data = {'created_dt': 'test1'}
    response = superuser_client.patch(
        f'/api/private/dish/{dish.id}', data=data, content_type="application/json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_dish(superuser_client, dish):
    response = superuser_client.delete(
        f'/api/private/dish/{dish.id}', content_type="application/json")

    assert response.status_code == 204
    assert not Dish.objects.all().exists()


@pytest.mark.django_db
def test_create_dish_attachment_success(superuser_client, dish):
    data = {
        "id": dish.id,
    }

    file1_content = b'Test file content 1'

    file1 = SimpleUploadedFile("file1.txt", file1_content)

    data = {
        "id": dish.id,
        'files': file1,
    }

    response = superuser_client.post('/api/private/dish/add-attachemnt', data, format='multipart')

    assert response.status_code == 201
    assert DishAttachment.objects.count() == 1
    assert response.data['message'] == "success"
