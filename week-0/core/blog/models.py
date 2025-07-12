from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post (models.Model):
    
    
    class Status(models.TextChoices):
        # code /data base / show user
        DRAFT = 'DF', 'draft'
        PUBLISHED = 'PB', 'published'
        REJECTED = 'RJ','rejected'

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    title = models.CharField(max_length=50)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_posts')
    
    
    def __str__(self):
        return self.title
    
    # tune the class
    class Meta:
        ordering = ['-publish']
        # indexing work in django model but have downfall of cpu proses
        indexes = [models.Index(fields=['publish'])]