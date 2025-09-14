from django import template
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe
from ..models import Post, Comment
register = template.Library()

@register.simple_tag()
def total_posts():
    return Post.published.count()
@register.simple_tag()
def total_comments():
    return Comment.objects.filter(is_active=True).count()

@register.simple_tag()
def last_post_date():
    return Post.published.order_by('-created')[0].created

@register.inclusion_tag('partials/latest-post.html')
def latest_post(count=5):
    posts = Post.published.order_by('-created')[:count]
    context = {'posts': posts}
    return context


@register.simple_tag()
def most_popular_posts(count=5):
    return Post.published.annotate(num_comments=Count('comments')).order_by('-num_comments')[:count]


@register.filter(name='markdown')
def to_markdown(value):
    return mark_safe(markdown(value))