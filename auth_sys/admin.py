from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Используем стандартный UserAdmin, чтобы были поля пароля и прав
admin.site.register(User, UserAdmin)