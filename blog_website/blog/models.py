# blog/models.py
from django.db import models
from django.contrib.auth.models import User
import markdown
from autoslug import AutoSlugField
from django.urls import reverse

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Economics', 'Economics'),
        ('Environment', 'Environment'),
        ('Science', 'Science'),
        ('Technology', 'Technology'),
        ('International Relations', 'International Relations'),
        ('History', 'History'),
        ('Indian Polity', 'Indian Polity'),
        ('Geography', 'Geography'),
        ('Current Affairs', 'Current Affairs'),
        ('Indian Society', 'Indian Society'),
        ('Governance', 'Governance'),
        ('Disaster Management', 'Disaster Management'),
        ('Internal Security', 'Internal Security'),
        ('Social Justice', 'Social Justice'),
        ('Agriculture', 'Agriculture'),
        ('General Science', 'General Science'),
        ('Indian Heritage', 'Indian Heritage'),
        ("PYQ's", "PYQ's")
    ]
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True)
    content = models.TextField()
    content_html = models.TextField(editable=False, blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General Science')

    def save(self, *args, **kwargs):
        if self.content:
            self.content_html = markdown.markdown(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_snippet(self):
        if self.content_html:
            return self.content_html[:200] + '...' if len(self.content_html) > 200 else self.content_html
        return self.content[:200] + '...' if len(self.content) > 200 else self.content

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})