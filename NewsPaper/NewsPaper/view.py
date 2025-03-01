from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views import View
from django.http.response import HttpResponse
from django.utils import timezone
from django.shortcuts import redirect
import pytz

@cache_page(60)
def home_page(request):
    """View main page"""
    return render(request, template_name='index.html', context={})

class Index(View):
    def get(self, request):
        curent_time = timezone.now()

        context = {
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'time.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('time')