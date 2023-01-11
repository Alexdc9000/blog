from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost
from .forms import BlogPostForm

# Create your views here.
def check_post_owner(request, post):
    if post.owner != request.user:
        raise Http404


def index(request):
    """"""
    posts = BlogPost.objects.order_by('-date_added')
    context = {'posts':posts}
    return render(request, 'blogs/index.html', context) 


@login_required
def new_post(request):
    """"""
    if request.method != 'POST':
        form = BlogPostForm() 

    else:
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            # form.save()
            return redirect('blogs:index')

    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, post_id):
    """"""
    post = BlogPost.objects.get(id=post_id)
    check_post_owner(request, post)
        
    if request.method != 'POST':
        form = BlogPostForm(instance=post)

    else:
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():

            form.save()
            return redirect('blogs:index')

    context = {'post': post, 'form':form}
    return render(request, 'blogs/edit_post.html', context)