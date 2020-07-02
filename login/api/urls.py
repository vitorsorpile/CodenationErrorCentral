from django.urls import path
from login.api.views import(
        register_view,
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'user'

urlpatterns = [
        path('register', register_view),
        path('login', obtain_auth_token),
]