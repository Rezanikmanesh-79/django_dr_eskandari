from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter

# admin.site.site_header = 'پنل مدیریت جنگو'
# admin.site.site_title = 'پنل مدیریت وبلاگ'
# admin.site.index_title = 'مدیریت وبلاگ'
# admin.site.register(Post)

class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'author', 'publish', 'status','read_time']
    ordering = ('title','-publish',)
    list_filter = ('status','author',('publish', JDateFieldListFilter))
    search_fields = ('title','content')
    # raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug':('title',)}
    list_editable = ['status', 'read_time']
    list_display_links = ['title','author']

    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name','subject','phone','created_at']
    ordering =['-created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','name','created_at','is_active']
    ordering = ('-created_at',)
    list_filter = ('is_active',('created_at',JDateFieldListFilter))
    search_fields = ('content','name',)
    list_editable = ['is_active',]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id','post','title','created_at']
    ordering = ('post',)



