from django.contrib import admin

from posts.models import Post, Tag, Category, Comment, Friend

# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Friend)
