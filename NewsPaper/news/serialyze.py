from rest_framework import serializers
from .models import Post

class PostSerialyzes(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text_post', 'choice_categories']