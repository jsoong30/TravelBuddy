from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name='home'),
    path('itinerary/', views.itinerary, name='itinerary'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]
