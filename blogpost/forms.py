
from django import forms
from .models import Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
        widgets = {'text': SummernoteWidget(),}

