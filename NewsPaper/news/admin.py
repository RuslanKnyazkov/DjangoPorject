from django.contrib import admin
from .models import Post, Author, Comment, PostCategory, Category, CategorySubscribers
from modeltranslation.admin import TranslationAdmin

class PostAdmin(TranslationAdmin):
    model = Post

class PostAdmin(TranslationAdmin):
    model = Category

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostCategory)
admin.site.register(CategorySubscribers)

