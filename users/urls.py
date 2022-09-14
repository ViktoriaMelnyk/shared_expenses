from django.urls import path
from .views import *


urlpatterns = [
    path('login/', UserLogin.as_view(), name='login-user'),
    path('logout/', UserLogout.as_view(), name='logout-user'),
    path('register/', SignUp.as_view(), name='register-user'),
]