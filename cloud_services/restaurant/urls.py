from django.urls import path
from restaurant.views import MenuGenericAPI, DishGenericAPI, list_menu

urlpatterns = [
    path('private/menu', MenuGenericAPI.as_view()),
    path('private/menu/<int:pk>', MenuGenericAPI.as_view()),
    path('private/dish', DishGenericAPI.as_view()),
    path('private/dish/<int:pk>', DishGenericAPI.as_view()),
    
    path('public/menu', list_menu),
]