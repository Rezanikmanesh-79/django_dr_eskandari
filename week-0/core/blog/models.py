from django.db import models
from django_jalali.db import models as jmodels
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# for django resize 
from django_resized import ResizedImageField
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
    reading_time=models.PositiveIntegerField(default=5,verbose_name='زمان مطالعه')
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    publish = jmodels.jDateTimeField(default=timezone.now)
    # related_name take all of targeted user post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts',verbose_name="نویسنده")
    # over writing the post class urls for dynamic url
    def get_absolute_url(self):
        return reverse('blog:post-detail',args=[self.id])
    
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

class Ticket(models.Model):
    message = models.TextField(verbose_name="متن تیکت")
    name = models.CharField(max_length=50,null=True,blank=True,verbose_name="نام")
    email = models.EmailField(null=True,blank=True,verbose_name="ایمیل")
    phone = models.CharField(max_length=11,null=True,blank=True,verbose_name="تلفن")
    subject = models.CharField(max_length=50,verbose_name="موضوع")
    created_at=jmodels.jDateTimeField(verbose_name="تاریخ ثبت درخواست",auto_now_add=True)
    
    def __str__(self):
        return self.subject

    class Meta:
        verbose_name='تیکت'
        verbose_name_plural='تیکت ها'

class Comment(models.Model):
    # with "related_name" we can use "post.comment"
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment',verbose_name="کامنت")
    name=models.CharField(max_length=50,verbose_name="نام نویسنده")
    email=models.EmailField(verbose_name="ایمیل")
    content=models.TextField(verbose_name="متن دیدگاه")
    created_at=jmodels.jDateTimeField(auto_now_add=True,verbose_name='ساخته شده در')
    update_at=jmodels.jDateTimeField(auto_now=True,verbose_name='اپدیت شده در')
    is_active=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    class Meta:
        ordering=['-created_at']
        indexes=[models.Index(fields=["-created_at"])]
        verbose_name="دیدگاه"
        verbose_name_plural="دیدگاه ها"

# we need too create class for images
class Image(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='تصاویر'
    )
    # come from django_resized
    image = ResizedImageField(
        upload_to='images/',
        verbose_name="تصویر",
        size=[300, 300],
        crop=['middle', 'center'],quality=50
    )
    description = models.TextField(verbose_name="توضیحات")
    created_at = jmodels.jDateTimeField(auto_now_add=True,verbose_name="ساخته شده در")

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"
        ordering = ['-created_at']
