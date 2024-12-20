from django.forms import DateInput, TextInput
from django_filters import (FilterSet, CharFilter,DateFilter)

from .models import Post


class PostFilter(FilterSet):
    name = CharFilter(widget = TextInput(attrs={'class': 'form-control'}),
                      field_name='author_post__name__username', lookup_expr='iexact',
                      label='Имя автора')
    title = CharFilter(widget = TextInput(attrs={'class': 'form-control'}),
                       field_name='title', label='Заголовок', lookup_expr='startswith')
    date = DateFilter(widget=DateInput(attrs={'type': 'date'}), lookup_expr='gt',
                          field_name='create_date', label='Дата поста не  позже')

    class Meta:
        model = Post
        fields = ['name', 'title', 'date']

