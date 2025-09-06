from django.contrib import admin
from blog.models import Post,Ticket,Comment,Image
from django_jalali.admin.filters import JDateFieldListFilter

admin.site.site_header = "پنل مدیریت جنگو"
admin.site.site_title = "پنل مدیریت وبلاگ"
admin.site.index_title = "خوش آمدید به پنل مدیریت"


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    # this ordering will not change data base
    ordering = ['-publish']
    list_filter = ('status', 'author',('publish', JDateFieldListFilter))
    
    search_fields = ('title', 'content')
    # add user id instead of name
    raw_id_fields = ('author', )
    # archiving post by date
    date_hierarchy = 'publish'
    # automating naming of slug
    prepopulated_fields = {'slug': ('title',)}
    # editing status on main page
    list_editable = ('status',)
    list_display_links = ['title', 'author']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display=['name','email','phone','subject','created_at']
    ordering = ['-created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['post','name','created_at','is_active']
    ordering=('-created_at',)
    list_filter=('is_active',('created_at',JDateFieldListFilter))
    search_fields=('content','name')
    list_editable=['is_active']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display=['id','post','image']