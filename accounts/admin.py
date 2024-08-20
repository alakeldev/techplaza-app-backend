from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    """
    Custom admin class for the User model.
    Displays the email, full name, verification status,
    and date joined in the admin list view.
    Allows filtering by verification status and date joined.
    Enables searching by email and full name.
    Orders the users by date joined in descending order.
    """

    list_display = ("email", "full_name", "is_verified", "date_joined")
    list_filter = ("is_verified", "date_joined")
    search_fields = ("email", "full_name")
    ordering = ("-date_joined",)


admin.site.register(User, UserAdmin)
