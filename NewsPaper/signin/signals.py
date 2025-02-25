from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, slug=slugify(instance.username),
                               firstname=instance.first_name, lastname=instance.last_name)
        html_content = render_to_string(
            'email_confirmation_signup_message.html',
            {'user': instance}
        )
        mail_content = EmailMultiAlternatives(
            subject=f'{instance.username}',
            from_email='rus.knyazkov.94@mail.ru',
            to=[f'{instance.email}']
        )
        mail_content.attach_alternative(html_content,
                                        'text/html')
        mail_content.send()