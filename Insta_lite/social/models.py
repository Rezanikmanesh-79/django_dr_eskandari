from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# from django.utils.text import slugify
from taggit.managers import TaggableManager

class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='account_images/', blank=True,
                              null=True)
    job = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    

class Post(models.Model):
    
    title = models.CharField(max_length=50, verbose_name="عنوان")
    content = models.TextField()
    tags = TaggableManager(blank=True)
    # slug = models.SlugField(unique=True)
    

    # date fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    # relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name="نویسنده")


    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, verbose_name="لایک‌ها")

    save_by=models.ManyToManyField(User, related_name='saved_posts', blank=True)

    def get_absolute_url(self):
        return reverse('social:post-detail', args=[self.id])

    def __str__(self):
        return f'{self.title} by {self.author.username}'

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)

        super().delete(*args, **kwargs)
    
    class Meta:
        ordering = ['-created']

        indexes = [models.Index(fields=['-created'])]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'




