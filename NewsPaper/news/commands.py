from models import Author, Post, Comment, Category, PostCategory
from django.contrib.auth.models import User

user1 = User.objects.create_user('Валентин')
user2 = User.objects.create_user('Леонид')

author1 = Author.objects.create(name=user1)
author2 = Author.objects.create(name=user2)

category1 = Category.objects.create(name_categories='спорт')
category2 = Category.objects.create(name_categories='образование')
category3 = Category.objects.create(name_categories='политика')
category4 = Category.objects.create(name_categories='финансы')

article1 = Post.objects.create(author_post=author1, choice_categories='article',
                               title='Что такое Django',
                               text_post='Django — это высокоуровневый веб-фреймворк для языка программирования Python,'
                                         ' который позволяет быстро и эффективно разрабатывать веб-приложения.'
                                         ' Он был создан для упрощения процесса разработки и предоставления'
                                         ' разработчикам инструментов для создания мощных и масштабируемых веб-сайтов.'
                                         ' Основная цель Django — сделать разработку веб-приложений быстрой и приятной,'
                                         ' предоставляя готовые решения для общих задач.')

article2 = Post.objects.create(author_post=author2, choice_categories='article',
                               title='Девальвация.',
                               text_post='Девальва́ция снижение курса национальной валюты по отношению к твёрдым валютам'
                                         ' в системах с фиксированным курсом валюты,'
                                         ' устанавливаемым денежными властями.')

news = Post.objects.create(author_post=Author.objects.get(id=8),
                           choice_categories='news', title='Игры будущего в Казани',
                           text_post='В октябре 2023 года в Казани прошли международные игры'
                                     ' «Фиджитал лайв» в формате турнира «Игры будущего».'
                                     ' Они состоялись в павильоне выставочного центра «Казань Экспо».'
                                     '9 и 10 октября прошли соревнования по фиджитал-баскетболу '
                                     '(интерактивный баскетбол (видеоигра NBA2K) + баскетбол 3х3).'
                                     ' Участники соревновались в виртуальном пространстве,'
                                     ' используя специальные сенсорные перчатки и очки виртуальной реальности.'
                                     '21–22 октября прошли соревнования дисциплины фиджитал-лазертаг '
                                     '«фиджитал тактический бой» (CS: GO + лазертаг),'
                                     ' «фиджитал тактический бой» (Warface + лазертаг).'
                                     ' Игроки использовали лазерные пистолеты для демонстрации своей ловкости и'
                                     ' стратегического мышления.'
                                     'Мастера фиджитал-дисциплин сначала сражались в видеоиграх,'
                                     ' а затем продолжали борьбу на реальных спортивных площадках. ')

article1.like()
article1.like()
article1.like()
article2.like()
article2.like()
news.like()
news.like()
news.dislike()

post_cat1 = PostCategory.objects.create(post_id=article1, category_id=category2)
post_cat2 = PostCategory.objects.create(post_id=article2, category_id=category3)
post_cat3 = PostCategory.objects.create(post_id=article2, category_id=category4)
post_cat4 = PostCategory.objects.create(post_id=news, category_id=category1)

com1 = Comment.objects.create(name_user=user1,
                              current_post=news,
                              text='Хотелось бы там побывать, но не получилось',
                              )
com2 = Comment.objects.create(name_user=user2,
                              current_post=article1,
                              text='Не легкий путь по ее изучению предстоит вам')

com3 = Comment.objects.create(name_user=user1,
                              current_post=article2,
                              text='Да раньше пачка Winston стоила 30 рублей,'
                                   'а теперь страшно представить!!!')

com4 = Comment.objects.create(name_user=user2,
                              current_post=article2,
                              text='И я помню те времена')

com5 = Comment.objects.create(name_user=user1,
                              current_post=article1,
                              text='Автор, пожалуйста сделай более подробное описание')

com1.like()
com2.like()
com3.like()
com3.like()
com3.dislike()
com4.like()
com5.like()
com5.like()
com5.like()

author1.update_rating()
author2.update_rating()

best_author = Author.objects.order_by('-rating_user').values('name__username', 'rating_user').first()

best_post = Post.objects.order_by('-rating_post').values('create_date', 'author_post__name__username',
                                                         'rating_post', 'title', 'id').first()
best_preview = Post.objects.filter(id=best_post['id'])
print(best_post, best_preview[0].preview())


all_comment_on_post = Post.objects.filter(id=best_post['id']).values('comments__name_user__username', 'comments__text',
                                              'comments__date_comment', 'comments__rating_comment')
