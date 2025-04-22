from django.urls import path, include

from . import views

urlpatterns = [
     path('', views.rooms_list, name='rooms_list'),
    path('<slug:slug>/', views.room, name='room'),
 ]