from django.urls import path
from errors.api.views import (
        api_get_delete_archive_error_view,
        api_create_error_view,
        ApiErrorListView,
        )

app_name = 'api'

urlpatterns = [
    path('<int:error_id>', api_get_delete_archive_error_view, name='error'),
    path('create', api_create_error_view, name='create'),
    path('list', ApiErrorListView.as_view(), name='list'),
]