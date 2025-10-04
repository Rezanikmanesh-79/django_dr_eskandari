from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from social.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number')

    fieldsets = (
        ('Additional Info', {
            'fields': (
                'first_name',
                'last_name',
                'bio',
                'job',
                'date_of_birth',
                'photo',
                'phone_number',
            )
        }),
    )
