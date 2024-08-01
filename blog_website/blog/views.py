from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        'author': 'saurav tripathi',
        'title': 'Blog Post 1 ',
        'content': 'First post in django',
        'date_posted': 'August 27 90392'
    },
    {
        'author': 'saurav tripathi',
        'title': 'Post 2  ',
        'content': 'Second test post',
        'date_posted': 'July 12 1832'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

