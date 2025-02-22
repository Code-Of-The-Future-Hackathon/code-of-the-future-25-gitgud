from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('manage/food-water/<id>/', views.manage_food_water, name='manage_food_water'),
    path('manage/door/<id>/', views.manage_door, name='manage_door'),
    path('manage/door/manual/<id>/', views.manual_door, name='manual_door'),
    path('manage/location/<id>/', views.manage_location, name='manage_location'),
]