from django.urls import path
from errors.api.views import (
        api_detail_error_view,
        api_delete_error_view,
        api_update_error_view,
        api_create_error_view,
        api_archive_error_view,
        )

app_name = 'api'

urlpatterns = [
    path('<int:error_id>', api_detail_error_view),
    path('<int:error_id>/archive', api_archive_error_view),
    path('<int:error_id>/delete', api_delete_error_view),
    path('<int:error_id>/update', api_update_error_view),
    path('create', api_create_error_view)
]