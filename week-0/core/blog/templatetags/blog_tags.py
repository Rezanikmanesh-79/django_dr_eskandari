from django import template
from blog.models import Post, Comment
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe
register = template.Library()
# in this method sever just calc once 


# simple_tag() is fo one var
@register.simple_tag()
def total_post():
    return Post.published.count()

@register.simple_tag()
def total_comments():
    return Comment.objects.filter(is_active=True).count()
@register.simple_tag()
def last_post_date():
    return Post.published.order_by('-created')[0].created
# we should tell the location in ()
# we use inclusion_tag when we have list of var
@register.inclusion_tag('partials/latest-post.html')
def latest_post(count=5):
    posts=Post.published.order_by('-created')[:count]
    context={"posts":posts}
    return context

@register.simple_tag()
def most_popular_post(count=5):
    return (
        Post.published
        .annotate(num_comments=Count("comment"))  
        .order_by("-num_comments")[:count]
    )
@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))