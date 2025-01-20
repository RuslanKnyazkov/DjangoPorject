from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache

class Author(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.IntegerField(default=0, db_column='rating_user')

    def update_rating(self):
        sum_author_rating_post = self.post_set.all().aggregate(rating_sum=Sum('rating_post'))
        sum_rating_own_comments = Comment.objects.filter(name_user=self.name_id).aggregate(
            sum_own_comment=Sum('rating_comment'))
        sum_all_comment = self.post_set.all().aggregate(sum_comment=Sum('comments__rating_comment'))
        self.rating_user = sum_author_rating_post['rating_sum'] * 3 + sum_rating_own_comments['sum_own_comment'] \
                           + sum_all_comment['sum_comment']
        self.save()
        return f'Рэйтинг {self.name} : {self.rating_user}'

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    NAME_CATEGORIES = [
        ('спорт', 'sport'),
        ('политика', 'politic'),
        ('образование', 'studying'),
        ('финансы', 'finance')
    ]
    name_categories = models.CharField(max_length=11,
                                       choices=NAME_CATEGORIES, default='образование')
    subscribers = models.ManyToManyField(User, default=None, through='CategorySubscribers')

    def __str__(self):
        return f'{self.name_categories}'

class CategorySubscribers(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

class Post(models.Model):
    NAME_POST = [
        ('новость', 'news'),
        ('статья', 'article')
    ]
    author_post = models.ForeignKey(Author, verbose_name='Пост автора',
                                    on_delete=models.CASCADE)

    create_date = models.DateTimeField(verbose_name='Дата создания',
                                       auto_now_add=True)

    choice_categories = models.CharField(max_length=7,
                                         choices=NAME_POST,
                                         default='news')

    test = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    title = models.CharField(max_length=255, unique=True, verbose_name='Заголовок')
    text_post = models.TextField(verbose_name='Текст')
    rating_post = models.IntegerField(default=0, db_column='rating_post')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('single_news', kwargs={"pk": self.pk})


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(self.get_absolute_url())

    def preview(self):
        return f'{self.text_post[:124]}...'

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def tests(self):
        return self.comments.all()


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_id}. Категория {self.category_id}'


class Comment(models.Model):  # completed
    name_user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_post = models.ForeignKey(Post, on_delete=models.CASCADE,
                                     related_name='comments')
    text = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0, db_column='rating_comment')

    def __str__(self):
        return f'Заголовок статьи :{self.current_post.title}'

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        if self.rating_comment == 0:
            pass
        else:
            self.rating_comment -= 1
            self.save()



