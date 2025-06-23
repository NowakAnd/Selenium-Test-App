from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PostForm
from .models import Post

def home_view(request):
    return render(request, 'home.html')

def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post_list.html', {'posts' : posts})

@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})