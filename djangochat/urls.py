from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.rooms_list,           name='rooms_list'),
    path('create/', views.create_room, name='create_room'),
    path('<slug:slug>/',      views.room,                 name='room'),
    path('<slug:slug>/join/', views.request_to_join,      name='request_to_join'),
    path('<slug:slug>/requests/',
         views.manage_requests,        name='manage_requests'),
    path('<slug:slug>/requests/<int:membership_id>/<int:new_status>/',
         views.change_request_status, name='change_request_status'),
]