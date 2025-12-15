from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


# ================================================================
#                         Custom User Model
# ================================================================

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Includes additional fields for profile info, social interactions,
    and relationships such as following, blocking, and reporting.
    """

    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='account_images/', null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)

    # NOTE:
    # AbstractUser already has "date_joined" (DateTimeField)
    # برای جلوگیری از تداخل، آن را override نمی‌کنیم.
    join_date = models.DateField(auto_now_add=True, verbose_name="تاریخ عضویت")

    # Follow system (one-directional): A follows B
    following = models.ManyToManyField(
        'self',
        through='Contact',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    # Blocking system
    blocked_users = models.ManyToManyField(
        'self',
        through='BlockRelation',
        symmetrical=False,
        related_name='blocked_by',
        blank=True
    )

    # Report system (direct many-to-many without through)
    reported_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='reported_by',
        blank=True
    )

    # ------------------------------------------------------------
    #                      Utility Methods
    # ------------------------------------------------------------

    def has_blocked(self, other_user):
        """Check if this user has blocked another user (efficient query)."""
        return self.blocked_users.filter(id=other_user.id).exists()

    def is_blocked(self, other_user):
        """Check if this user is blocked by another user."""
        return other_user.blocked_users.filter(id=self.id).exists()

    def get_absolute_url(self):
        """Profile URL."""
        return reverse("social:user_detail", kwargs={"username": self.username})

    def __str__(self):
        return self.username


# ================================================================
#                            Post Model
# ================================================================

class Post(models.Model):
    """
    Represents user-generated content (educational posts).
    Includes tags, likes, saves, and image handling.
    """

    title = models.CharField(max_length=50, verbose_name="عنوان")
    content = models.TextField()
    tags = TaggableManager(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_posts',
        verbose_name="نویسنده"
    )

    # Social interactions
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    save_by = models.ManyToManyField(User, related_name='saved_posts', blank=True)

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_absolute_url(self):
        return reverse("social:post_detail", args=[self.id])

    def delete(self, *args, **kwargs):
        """
        Safely deletes image files related to the post before deleting the post itself.
        Uses Django API instead of raw storage.path for safety with cloud storage.
        """
        for img in self.images.all():
            if img.image_file:
                img.image_file.delete(save=False)

        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"


# ================================================================
#                 Follow Model (Contact / Relation)
# ================================================================

class Contact(models.Model):
    """
    Through model for implementing follow system:
    user_from follows user_to
    """

    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        # Prevent duplicate follow records
        constraints = [
            models.UniqueConstraint(
                fields=['user_from', 'user_to'],
                name='unique_follow_relation'
            )
        ]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


# ================================================================
#                 User Reporting System
# ================================================================

class Report(models.Model):
    """
    User A reports user B.
    Used for moderation and safety management.
    """

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='reports_made',
        on_delete=models.CASCADE
    )

    reported = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='reports_received',
        on_delete=models.CASCADE
    )

    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One user should not be able to report another user repeatedly
        constraints = [
            models.UniqueConstraint(
                fields=['reporter', 'reported'],
                name='unique_user_report'
            )
        ]

    def __str__(self):
        return f"{self.reporter} reported {self.reported}"


# ================================================================
#                     User Blocking System
# ================================================================

class BlockRelation(models.Model):
    """
    Middleware table for user blocking system.
    """

    blocker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='blocker_set',
        on_delete=models.CASCADE
    )

    blocked = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='blocked_set',
        on_delete=models.CASCADE
    )

    blocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate block records
        constraints = [
            models.UniqueConstraint(
                fields=['blocker', 'blocked'],
                name='unique_block_relation'
            )
        ]

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"

