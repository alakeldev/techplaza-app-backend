from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_verified', 'date_joined')
    list_filter = ('is_verified', 'date_joined')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)

admin.site.register(User, UserAdmin)