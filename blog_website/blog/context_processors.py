# blog/context_processors.py
from .models import Post

def categories(request):
    categories = Post.CATEGORY_CHOICES
    return {'categories': [choice[0] for choice in categories]}
