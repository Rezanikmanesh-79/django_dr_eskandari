from django.contrib import admin
from .models import User, Post
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'phone',
                    ]
    readonly_fields = ['date_joined', ]
    # list_editable = ['first_name', 'last_name', 'phone', ]
    fieldsets = (
        ('Additional Info', {
            "fields": ('email','bio', 'job', 'date_of_birth','date_joined', 'photo',
                
            ),
        }),
    )
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'updated']
    search_fields = ['title', 'content']
    list_filter = ['created', 'author']
    # prepopulated_fields = {'slug': ('title',)}
