from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

# Register your models here.

class PostiAdmin(SummernoteModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'text', 'uuid', 'user']}),
        ('Date published', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('title', 'pub_date')
    summernote_fields = ('text',)
    readonly_fields = ['uuid', 'user']


admin.site.register(Post, PostiAdmin)
