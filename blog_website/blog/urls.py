from django.urls import path
from .views import( PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    UploadMarkdownView,
                    CategoryPostListView,
					search,
                    robots_txt,
					upload_markdown,
                    )
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('upload/', UploadMarkdownView.as_view(), name='upload-markdown'),
    #path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('robots.txt', robots_txt, name='robots-txt'),
    path('category/<str:category>/', CategoryPostListView.as_view(), name='category-posts'),
	path('search/', search, name='search'),
	path('api/upload/', upload_markdown, name='api-upload-markdown'),
]

