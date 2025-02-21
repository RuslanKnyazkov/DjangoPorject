from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, User

@receiver(post_save, sender=Post)
def foo(sender, created, instance, **kwargs):
    post = Post.objects.all().order_by('-create_date')[1]

    if created:
        for cat in post.test.all():
            users = User.objects.filter(category=cat)
            for user in users:
                html_content = render_to_string(
                    'notification.html',
                    {'user': user, 'post': post, 'cat' : cat}
                )
                mail_content = EmailMultiAlternatives(
                    subject=f'{user.username}',
                    body=f'В разделе {cat} появилась новая запись',
                    from_email='rus.knyazkov.94@mail.ru',
                    to=[f'{user.email}']
                )
                mail_content.attach_alternative(html_content,
                                                'text/html')
                mail_content.send()
    else:
        mail_content = EmailMultiAlternatives(
            subject=f'',
            body=f'В разделе появилась новая запись',
            from_email='rus.knyazkov.94@mail.ru',
            to=['rus.knyazkov.94@mail.ru']
        )
        mail_content.send()


