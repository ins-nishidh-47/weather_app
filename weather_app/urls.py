from django.urls import path
from .views import index, delete_city

urlpatterns = [
    path("", index, name="index"),
    path("delete/<str:city_name>/", delete_city, name="delete_city"),
]
