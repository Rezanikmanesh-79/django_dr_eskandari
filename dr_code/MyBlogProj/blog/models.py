from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify


# Custom Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'draft'
        PUBLISHED = 'PB', 'published'
        REJECTED = 'RJ', 'rejected'

    CATEGORY_CHOICES = (
        ('technology','technology'),
        ('programming','programming'),
        ('ai','ai'),
        ('other','other'),
    )
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES,default='other')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, verbose_name='وضعیت')
    title = models.CharField(max_length=50, verbose_name="عنوان")
    content = models.TextField()
    slug = models.SlugField(unique=True)
    read_time = models.IntegerField(default=5, verbose_name='مطالعه')

    # date fields
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    publish = jmodels.jDateTimeField(default=timezone.now)

    # relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name="نویسنده")

    objects = jmodels.jManager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[self.id])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for img in self.images.all():
            storage, path = img.image_file.storage, img.image_file.path
            storage.delete(path)

        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-publish']

        indexes = [models.Index(fields=['-publish'])]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'


class Ticket(models.Model):
    message = models.TextField(verbose_name="متن تیکت")
    name = models.CharField(max_length=50, verbose_name="نام ثبت کننده", null=True, blank=True)
    email = models.EmailField(verbose_name="ایمیل", null=True, blank=True)
    phone = models.CharField(max_length=11, verbose_name="تلفن")
    subject = models.CharField(max_length=50, verbose_name="موضوع")
    created_at = jmodels.jDateTimeField(verbose_name='تاریخ دثبت در خواست', auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.subject}"

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="پست")
    name = models.CharField(max_length=50, verbose_name="نام نویسنده")
    email = models.EmailField(verbose_name="ایمیل", null=True, blank=True)
    content = models.TextField(verbose_name="متن دیدگاه")
    created_at = jmodels.jDateTimeField(verbose_name=' تاریخ درج', auto_now_add=True)
    updated_at = jmodels.jDateTimeField(verbose_name=' تاریخ ویرایش', auto_now=True)
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')

    def __str__(self):
        return f"{self.id}: {self.name},{self.post}"

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name="تصویر")
    image_file = ResizedImageField(upload_to='images/', verbose_name="تصویر", size=[300, 300],
                                   crop=['middle', 'center'], quality=50)
    title = models.CharField(max_length=50, verbose_name="عنوان تصویر", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created_at = jmodels.jDateTimeField(verbose_name='تاریخ آپلود', auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.title}"

    def delete(self, *args, **kwargs):
        storage, path = self.image_file.storage, self.image_file.path
        storage.delete(path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

class Account(models.Model):
    user = models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    date_of_birth=jmodels.jDateTimeField(blank=True,null=True)
    bio = models.TextField(null=True, blank=True)
    job = models.CharField(max_length=100,null=True, blank=True)
    photo = ResizedImageField(upload_to='account_image', size=[500,500],quality=75, crop=['middle', 'center'],blank=True,null=True)

    def __str__(self):
        return self.user.username
