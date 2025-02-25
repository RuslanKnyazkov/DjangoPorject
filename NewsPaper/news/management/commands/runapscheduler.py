import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives

from datetime import datetime, timedelta
from news.models import Post, User

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    users = User.objects.all()
    for user in users:
        for cat_id in user.categorysubscribers_set.all().values('category_id'):
            posts = Post.objects.filter(create_date__date__gt=datetime.today() - timedelta(days=7),
                                        test__id=cat_id['category_id'])
            html_content = render_to_string(
                'weekly_news.html',
                {'user': user, 'posts': posts}
            )
            mail_content = EmailMultiAlternatives(
                subject=f'Здравствуйте {user.username}. К вашему вниманию подборка'
                        f' постов по категориям за последнюю неделю. ',
                from_email='rus.knyazkov.94@mail.ru',
                to=[f'{user.email}']
            )
            mail_content.attach_alternative(html_content,
                                            'text/html')
            mail_content.send()


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='mon',hour='09', minute='00'),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
