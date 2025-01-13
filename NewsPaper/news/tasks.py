from datetime import datetime, timedelta
from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post


@shared_task
def start_user_notification():
    """
    Send mail all subscriber user at current category.
    """
    users = User.objects.all()
    for user in users:
        for cat_id in user.categorysubscribers_set.all().values('category_id'):
            posts = Post.objects.filter(create_date__date__gt=datetime.today() - timedelta(days=7),
                                        test__id=cat_id['category_id']).order_by('-create_date')[:3]
            print(posts)
            html_content = render_to_string(
                'weekly_news.html',
                {'user': user, 'posts': posts}
            )
            mail_content = EmailMultiAlternatives(
                subject=f'Здравствуйте {user.username}. К вашему вниманию подборка'
                        f'3 последних постов по категориям за последнюю неделю. ',
                from_email='rus.knyazkov.94@mail.ru',
                to=[f'{user.email}']
            )
            mail_content.attach_alternative(html_content,
                                            'text/html')
            mail_content.send()
