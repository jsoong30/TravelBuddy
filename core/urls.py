from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, signup
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', signup, name='signup'),
    path('', include('itineraries.urls')),
]
