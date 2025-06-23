from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

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

@require_POST
@login_required
def post_edit_ajax(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403)

    title = request.POST.get('title')
    content = request.POST.get('content')

    if not title or not content:
        return JsonResponse({'success': False, 'error': 'Title and content required.'})

    post.title = title
    post.content = content
    post.save()

    return JsonResponse({
        'success': True,
        'post': {
            'title': post.title,
            'content': post.content
        }
    })