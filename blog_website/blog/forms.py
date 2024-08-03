# blog/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class MarkdownUploadForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.md'):
            raise ValidationError('Invalid file type: only Markdown files are allowed.')
        return file
