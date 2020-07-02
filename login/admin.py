from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.models import User

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login', 'is_admin')
    search_fields = ('name', 'email')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, MyUserAdmin)