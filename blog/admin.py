from django.contrib import admin

from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'datetime_modified')
    ordering = ('status', '-datetime_modified')
    


# admin.site.register(Post, PostAdmin)

admin.site.register(Comment)
