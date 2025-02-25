from django.forms import DateInput, TextInput, CheckboxSelectMultiple
from django_filters import (FilterSet, CharFilter, DateFilter, ModelMultipleChoiceFilter)
from .models import Post, Category


class PostFilter(FilterSet):
    name = CharFilter(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя автора'}),
                      field_name='author_post__name__username', lookup_expr='iexact',
                      label='Имя автора')
    title = CharFilter(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Начало статьи'}),
                       field_name='title', label='Заголовок', lookup_expr='startswith')
    date = DateFilter(widget=DateInput(attrs={'type': 'date'}), lookup_expr='gt',
                      field_name='create_date', label='Дата поста не  позже')

    cat = ModelMultipleChoiceFilter(field_name='test', label='Категории',
                                    queryset=Category.objects.all(),
                                    widget=CheckboxSelectMultiple(attrs={}))

    class Meta:
        model = Post
        fields = ['name', 'title', 'date', 'cat']
