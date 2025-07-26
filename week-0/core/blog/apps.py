from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
    # Singular name for the model in the admin panel
    verbose_name = "بلاگ"