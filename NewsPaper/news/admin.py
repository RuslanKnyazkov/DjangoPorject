from django.contrib import admin
from .models import Post, Author, Comment, PostCategory, Category
# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostCategory)
