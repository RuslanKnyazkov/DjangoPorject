from django.apps import AppConfig


class SigninConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signin'

    def ready(self):
        import signin.signals
