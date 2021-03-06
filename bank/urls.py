from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
        Registration,
        RequestsCreate,
        RequestsView,
        UsersCreate,
        UsersView,
        

        )


urlpatterns = [
    path('register/',Registration,name='register'),
    path('user/<pk>/',UsersView,name='users'),
    path('users/',UsersCreate,name='users_create'),
    path('request/<pk>/',RequestsView,name='requests'),
    path('requests/',RequestsCreate,name='requests_create'),
    path('login/',obtain_auth_token,name='login'),
        ]
