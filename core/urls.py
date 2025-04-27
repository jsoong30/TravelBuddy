
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('signup/',views.signup,name='signup'),
    # Password reset:
    path(
      'accounts/password_reset/',
      auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
      name='password_reset'
    ),
    path(
      'accounts/password_reset/done/',
      auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
      name='password_reset_done'
    ),
    path(
      'accounts/reset/<uidb64>/<token>/',
      auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
      name='password_reset_confirm'
    ),
    path(
      'accounts/reset/done/',
      auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
      name='password_reset_complete'
    ),
    path('itinerary/', include('itineraries.urls'), name='itinerary'),
    path(
          'accounts/activate/<uidb64>/<token>/',
          views.activate,
          name='activate'
        ),
]