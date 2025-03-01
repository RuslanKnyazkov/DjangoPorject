from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text_post')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name_categories', ) # указываем, какие именно поля надо переводить в виде кортежа