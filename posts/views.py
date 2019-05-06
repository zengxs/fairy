from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import resolve

from posts.models import Post


# Create your views here.
def index(request):
    posts = Post.objects.order_by('-created_at').all()
    return render(request, 'posts/index.html', {'posts': posts})


def post(request, slug):
    p = get_object_or_404(Post, slug=slug)

    if not p.is_public and request.user != p.author:
        raise Http404

    should_route_name = 'page' if p.is_page else 'post'
    if resolve(request.path_info).url_name != should_route_name:
        redirect(should_route_name, slug=slug)

    return render(request, 'posts/post.html', {'post': p})