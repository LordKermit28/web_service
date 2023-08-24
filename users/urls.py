from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .views import VerifyEmailView
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify_email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('profile/genpassword/', views.generate_new_password, name='generate_new_password')
]

