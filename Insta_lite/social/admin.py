    # from django.contrib import admin
    # from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    # from django.utils.translation import gettext_lazy as _
    # from .models import User, Post, Contact, Report, BlockRelation


    # # ================================================================
    # #                        Admin: Custom User
    # # ================================================================

    # @admin.register(User)
    # class UserAdmin(BaseUserAdmin):
    #     """
    #     Custom admin for User model.
    #     Extends Django's built-in UserAdmin to include extra profile fields.
    #     """

    #     # What columns to show in the user list page
    #     list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'is_staff']

    #     # Fields that cannot be edited manually
    #     readonly_fields = ['date_joined', 'last_login']

    #     # Improve search ability
    #     search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']

    #     # Organize fields into sections
    #     fieldsets = (
    #         (_('Login Information'), {
    #             'fields': ('username', 'password')
    #         }),

    #         (_('Personal Info'), {
    #             'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'phone')
    #         }),

    #         (_('Profile Details'), {
    #             'fields': ('bio', 'job', 'photo')
    #         }),

    #         (_('Important Dates'), {
    #             'fields': ('date_joined', 'last_login')
    #         }),

    #         (_('Permissions'), {
    #             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
    #         }),

    #         (_('Relations'), {
    #             'fields': ('following', 'blocked_users', 'reported_users')
    #         }),
    #     )

    #     # Improve layout of fields when adding new users
    #     add_fieldsets = (
    #         (None, {
    #             'classes': ('wide',),
    #             'fields': ('username', 'email', 'password1', 'password2'),
    #         }),
    #     )

    #     # Filters on right sidebar
    #     list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']


    # # ================================================================
    # #                        Admin: Post Model
    # # ================================================================

    # @admin.register(Post)
    # class PostAdmin(admin.ModelAdmin):
    #     """
    #     Admin panel for posts.
    #     Shows metadata, filters, and read-only social fields.
    #     """

    #     list_display = ['id', 'title', 'author', 'created', 'updated']
    #     list_filter = ['created', 'author']
    #     search_fields = ['title', 'content']

    #     # Likes & saves should not be edited manually
    #     readonly_fields = ['likes_display', 'saved_by_display']

    #     def likes_display(self, obj):
    #         """
    #         Display liked users in a readable format.
    #         """
    #         return ", ".join(user.username for user in obj.likes.all())
    #     likes_display.short_description = "Liked by"

    #     def saved_by_display(self, obj):
    #         """
    #         Display users who saved the post.
    #         """
    #         return ", ".join(user.username for user in obj.save_by.all())
    #     saved_by_display.short_description = "Saved by"


    # # ================================================================
    # #        Extra Admin Pages (Optional but Highly Recommended)
    # # ================================================================

    # @admin.register(Contact)
    # class ContactAdmin(admin.ModelAdmin):
    #     """
    #     Show follow relationships in admin.
    #     Useful for debugging & analytics.
    #     """
    #     list_display = ['user_from', 'user_to', 'created']
    #     search_fields = ['user_from__username', 'user_to__username']
    #     list_filter = ['created']


    # @admin.register(Report)
    # class ReportAdmin(admin.ModelAdmin):
    #     """
    #     Admin panel for user reports.
    #     """
    #     list_display = ['reporter', 'reported', 'created_at']
    #     search_fields = ['reporter__username', 'reported__username']
    #     list_filter = ['created_at']


    # @admin.register(BlockRelation)
    # class BlockRelationAdmin(admin.ModelAdmin):
    #     """
    #     Admin panel for user blocking.
    #     """
    #     list_display = ['blocker', 'blocked', 'blocked_at']
    #     search_fields = ['blocker__username', 'blocked__username']
    #     list_filter = ['blocked_at']


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Post, Contact, Report, BlockRelation


# ================================================================
#                        Admin: Custom User
# ================================================================

class ContactInline(admin.TabularInline):
    """Inline for following relationships (User → User)."""
    model = Contact
    fk_name = 'user_from'   # show who this user follows
    extra = 0


class BlockRelationInline(admin.TabularInline):
    """Inline for blocked relationships (User → User)."""
    model = BlockRelation
    fk_name = 'blocker'     # show who this user has blocked
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for User model.
    Extends Django's built-in UserAdmin to include extra profile fields.
    """

    # What columns to show in the user list page
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone', 'is_staff']

    # Fields that cannot be edited manually
    readonly_fields = ['date_joined', 'last_login']

    # Improve search ability
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']

    # Organize fields into sections
    fieldsets = (
        (_('Login Information'), {
            'fields': ('username', 'password')
        }),

        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'phone')
        }),

        (_('Profile Details'), {
            'fields': ('bio', 'job', 'photo')
        }),

        (_('Important Dates'), {
            'fields': ('date_joined', 'last_login')
        }),

        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    # Improve layout of fields when adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # Filters on right sidebar
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']

    # Attach inlines for relations
    inlines = [ContactInline, BlockRelationInline]


# ================================================================
#                        Admin: Post Model
# ================================================================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin panel for posts.
    Shows metadata, filters, and read-only social fields.
    """

    list_display = ['id', 'title', 'author', 'created', 'updated']
    list_filter = ['created', 'author']
    search_fields = ['title', 'content']

    # Likes & saves should not be edited manually
    readonly_fields = ['likes_display', 'saved_by_display']

    def likes_display(self, obj):
        """Display liked users in a readable format."""
        return ", ".join(user.username for user in obj.likes.all())
    likes_display.short_description = "Liked by"

    def saved_by_display(self, obj):
        """Display users who saved the post."""
        return ", ".join(user.username for user in obj.save_by.all())
    saved_by_display.short_description = "Saved by"


# ================================================================
#        Extra Admin Pages (Optional but Highly Recommended)
# ================================================================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Show follow relationships in admin. Useful for debugging & analytics."""
    list_display = ['user_from', 'user_to', 'created']
    search_fields = ['user_from__username', 'user_to__username']
    list_filter = ['created']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin panel for user reports."""
    list_display = ['reporter', 'reported', 'created_at']
    search_fields = ['reporter__username', 'reported__username']
    list_filter = ['created_at']


@admin.register(BlockRelation)
class BlockRelationAdmin(admin.ModelAdmin):
    """Admin panel for user blocking."""
    list_display = ['blocker', 'blocked', 'blocked_at']
    search_fields = ['blocker__username', 'blocked__username']
    list_filter = ['blocked_at']