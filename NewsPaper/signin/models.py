from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Логин', on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255, verbose_name='Имя')
    lastname = models.CharField(max_length=255, verbose_name='Фамилия')
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='static/images/avatars/%Y/%m/%d/',
        default='static/images/avatars/default.jpg',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    def get_avatar(self):
        if not self.avatar:
            return '/static/images/avatars/default.jpg'
        return self.avatar.url

    def __str__(self):
        """
        Возвращение строки
        """
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.user_id})



