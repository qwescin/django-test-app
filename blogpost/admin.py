from django.contrib import admin

# Register your models here.

from .models import Post
from django_summernote.admin import SummernoteModelAdmin

class PostAdmin(SummernoteModelAdmin):
    fields = ['author', 'title', 'text', 'created_date', 'published_date']

admin.site.register(Post, PostAdmin)
#admin.site.register(SummernoteModelAdmin)

