"""error_central URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from login.views import login_view, register_view, logout_view
from errors.views import (index_view, add_error_view, delete_error_view,
                          archive_error_view, detail_error_view,
                          archived_errors_view)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('cadastro/', register_view, name='register'),
    path('logout/', logout_view),
    path('', index_view, name='index'),
    path('adderror/',add_error_view, name='add'),
    path('delete/<int:error_id>', delete_error_view, name='delete'),
    path('archive/<int:error_id>', archive_error_view, name='archive'),
    path('error/<int:error_id>', detail_error_view),
    path('archived/', archived_errors_view),
    #path('api/', include(('errors.urls', 'errors'), namespace='errors')),
    # path('accounts/', include('django.contrib.auth.urls')),


    path('api/error/', include('errors.api.urls', 'error_api')),
    path('api/auth/', include('login.api.urls', 'auth_api')),
]
