# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from algoliasearch.search_client import SearchClient
import markdown
import logging
from .models import Post
from .forms import MarkdownUploadForm
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from django.core.files.base import ContentFile


def get_categories():
    return dict(Post.CATEGORY_CHOICES)

def home(request):
    context = {
        'posts': Post.objects.all(),
        'categories': get_categories()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories()
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories()
        return context

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Post.objects.filter(category=category).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories()
        context['category'] = self.kwargs['category']
        return context

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories()
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories()
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = get_categories()
        return context

def about(request):
    return render(request, 'blog/about.html', {'title': 'About', 'categories': get_categories()})

class UploadMarkdownView(LoginRequiredMixin, View):
    def get(self, request):
        form = MarkdownUploadForm()
        return render(request, 'blog/upload_markdown.html', {'form': form, 'categories': get_categories()})

    def post(self, request):
        form = MarkdownUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            file = form.cleaned_data['file']
            category = form.cleaned_data['category']
            content = file.read().decode('utf-8')
            content_html = markdown.markdown(content)

            post = Post.objects.create(
                title=title,
                content=content,
                category=category,
                author=request.user
            )
            post.content_html = content_html  # Set the content_html field separately
            post.save()
            return redirect('post-detail', slug=post.slug)
        return render(request, 'blog/upload_markdown.html', {'form': form, 'categories': get_categories()})

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Sitemap: http://127.0.0.1:8000/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def search(request):
    query = request.GET.get('query', '')
    client = SearchClient.create(settings.ALGOLIA_APP_ID, settings.ALGOLIA_SEARCH_API_KEY)
    index = client.init_index(settings.ALGOLIA_INDEX_NAME)
    results = []
    if query:
        results = index.search(query)['hits']
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_markdown(request):
    title = request.data.get('title')
    category = request.data.get('category')
    file = request.FILES.get('file')

    if not title or not category or not file:
        return Response({"error": "Title, category, and file are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    content = file.read().decode('utf-8')
    
    post = Post(title=title, content=content, category=category, author=request.user)
    post.save()

    return Response({"success": "Post created successfully"}, status=status.HTTP_201_CREATED)