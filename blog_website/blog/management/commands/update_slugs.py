# blog/management/commands/update_slugs.py

from django.core.management.base import BaseCommand
from blog.models import Post
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Generate unique slugs for existing posts'

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        for post in posts:
            if post.slug == 'temp-slug' or not post.slug:
                post.slug = slugify(post.title + '-' + str(post.id))
                post.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated slugs for existing posts'))
