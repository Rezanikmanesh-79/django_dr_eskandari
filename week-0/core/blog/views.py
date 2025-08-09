from django.shortcuts import render ,get_object_or_404 ,redirect
from django.http import HttpResponse
from blog.models import Post,Ticket
import datetime
from django.core.paginator import Paginator , EmptyPage ,PageNotAnInteger
from blog.forms import TicketForm


def index(request):
    return HttpResponse("hello ")

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, per_page=2)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    # if user input some ting is not int
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'posts': page_obj}
    return render(request, 'blog/post-list.html', context)
def post_detail(request, pk):
    # try:
    #     post=Post.published.get(pk=pk)
    #     context = {"post":post}
    #     return render(request, template_name='blog/post-detail.html', context=context)
    # except:
    #     return HttpResponse('post dose not exist')
    
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)
    context = {"post":post,"new_date": datetime.datetime.now()}
    return render(request, template_name='blog/post-detail.html', context=context)

def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                message=cd['message'],
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject']
            )
            return redirect('blog:index')
    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form})