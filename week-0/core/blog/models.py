from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

'''
most imported data base command 
ddl--> drop -create
dml --> insert-update-delete
query --> select 
'''
# default manger for class a are objects exp : Post.objects.(get,filter,exclude)
# you can also build your custom manger like below class

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post (models.Model):

    class Status(models.TextChoices):
        # code /data base / show user
        DRAFT = 'DF', 'draft'
        PUBLISHED = 'PB', 'published'
        REJECTED = 'RJ', 'rejected'

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    # Singular name for the model in the admin panel
    title = models.CharField(max_length=50,verbose_name="عنوان")
    content = models.TextField()
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    # related_name take all of targeted user post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts',verbose_name="نویسنده")

    def __str__(self):
        return self.title

    # tune the class
    objects = models.Manager()
    published=PublishedManager()
    class Meta:
        # this ordering change data base
        ordering = ['-publish']
        # indexing work in django model but have downfall of cpu proses
        indexes = [models.Index(fields=['publish'])]

        # Singular name for the model in the admin panel
        verbose_name = "پست"
        # Plural name for the model in the admin panel
        verbose_name_plural = "پست ها"
# with __ you can access your class method exp: p= Post.objects.filter(author__first_name="reza")
