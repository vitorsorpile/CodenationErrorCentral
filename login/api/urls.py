from django.urls import path
from login.api.views import(
        register_view,
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'auth'

urlpatterns = [
        path('register', register_view, name='register'),
        path('login', obtain_auth_token, name='login'),
]