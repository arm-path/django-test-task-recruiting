import json

from django.contrib import messages
from django.db.models import Count, Q
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Recruit, Test, Planet, Sith
from .tasks import send_email_enrolled, send_email_excluded


class ValidationTest:
    def get(self, request, *args, **kwargs):
        """
            Проверяет urlpatterns --> test.
            1. Проверяет id(pk) рекрута в базе данных.
            2. Проверяет прохождение теста рекрутом, для предотвращения повторного прохождения,
            либо перехода по указанной ссылке третьими пользователями.
        """
        if Recruit.objects.filter(pk=self.kwargs['recruit_id']):
            if Recruit.objects.get(pk=self.kwargs['recruit_id']).trials is None:
                return super().get(request, *args, **kwargs)
        raise Http404

    def post(self, request, *args, **kwargs):
        """ Получение данных JSON, формирование результатов теста """
        if request.POST.get('questions') and request.POST.get('orden_code') is not None:
            orden_code = request.POST.get('orden_code')
            questions = json.loads(request.POST.get('questions'))
            try:
                if Test.objects.filter(orden_code=orden_code):
                    test = Test.objects.get(orden_code=orden_code)
                    trials = []
                    for question in questions:
                        trials.append(
                            {'question': question.get('question'),
                             'answer': question.get('answer'),
                             'correct_answer': test.question.get(pk=int(question.get('pk'))).answer
                             })
                    recruit = Recruit.objects.get(pk=kwargs.get('recruit_id'))
                    recruit.trials = trials
                    recruit.save()
                    return JsonResponse({'success': 'true'})
            except Exception as e:
                return JsonResponse({'success': 'false'})
        return JsonResponse({'success': 'false'})


class DetailMixin:
    def get(self, request, sith_id, planet_id=None, recruit_id=None, my_recruit_id=None):
        template = self.template
        sith = get_object_or_404(self.model, pk=sith_id)
        planets = Planet.objects.annotate(cnt=Count('recruit', filter=Q(recruit__enrolled=False)))

        if planet_id is not None:  # Фильтр по планетам и поиск по имени рекрута
            if not Planet.objects.filter(pk=planet_id):
                raise Http404
            if request.GET.get('search'):
                recruits = Recruit.objects.filter(planet=planet_id, enrolled=False,
                                                  name__icontains=request.GET.get('search'))
            else:
                recruits = Recruit.objects.filter(planet=planet_id, enrolled=False)
            page = f'Список рекрутов (Планеты: {Planet.objects.get(pk=planet_id)})'

        elif recruit_id is not None:  # Профиль рекрута и возможность зачислить в орден.
            if not Recruit.objects.filter(pk=recruit_id):
                raise Http404
            recruits = Recruit.objects.get(pk=recruit_id)
            page = f'Рекрут ({recruits.name})'
            template = self.template_recruit
        elif my_recruit_id is not None:  # Профиль рекрута ситха, и возможность удалить из ордена.
            if not Recruit.objects.filter(pk=my_recruit_id) or not sith.recruits.filter(pk=my_recruit_id).exists():
                raise Http404

            recruits = Recruit.objects.get(pk=my_recruit_id)
            page = f'Рекрут ({recruits.name})'
            template = 'django_applications/sith_page_my_recruit.html'

        else:  # Все планеты и поиск по имени рекрута
            recruits = Recruit.objects.filter(enrolled=False, name__icontains=request.GET.get('search')) \
                if request.GET.get('search') else Recruit.objects.filter(enrolled=False)
            page = 'Список рекрутов (Все)'

        context = {'sith': sith, 'planets': planets, 'recruits': recruits, 'title': f'Ситх {sith.name}', 'page': page}
        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        if kwargs.get('sith_id') and kwargs.get('recruit_id'):  # Запись рекрута в орден Руки тени
            if not Sith.objects.filter(pk=kwargs.get('sith_id')) or \
                    not Recruit.objects.filter(pk=kwargs.get('recruit_id')):
                raise Http404
            recruit = Recruit.objects.get(pk=kwargs.get('recruit_id'))
            sith = Sith.objects.get(pk=kwargs.get('sith_id'))
            if sith.recruits.count() < 3:  # Ограничения на количество Рук Тени у одного ситха. (Не более 3-ex)
                sith.recruits.add(recruit)
                recruit.enrolled = True
                recruit.save()
                send_email_enrolled.delay(recruit.email, sith.name)  # --> Celery Send mail
                messages.success(request, f'Рекрут " {recruit.name}"  успешно зачислен в орден Рук Тени!')
                return HttpResponseRedirect(reverse('sith_page', kwargs={'sith_id': kwargs.get('sith_id')}))
            else:
                messages.error(request, f'Превышен лимит рекрутов, не удалось зачислить рекрута: "{recruit.name}"')
                return HttpResponseRedirect(reverse('sith_page', kwargs={'sith_id': kwargs.get('sith_id')}))

        if kwargs.get('sith_id') and kwargs.get('my_recruit_id'):  # Удаление рекрута из ордена Руки тени
            if not Sith.objects.filter(pk=kwargs.get('sith_id')) or \
                    not Recruit.objects.filter(pk=kwargs.get('my_recruit_id')):
                raise Http404
            recruit = Recruit.objects.get(pk=kwargs.get('my_recruit_id'))
            sith = Sith.objects.get(pk=kwargs.get('sith_id'))
            if not sith.recruits.filter(pk=kwargs.get('my_recruit_id')).exists():
                raise Http404
            sith.recruits.remove(recruit)
            recruit.enrolled = False
            recruit.save()
            send_email_excluded.delay(recruit.email, sith.name)  # --> Celery Send mail
            messages.success(request, f'Рекрут " {recruit.name}"  успешно исключен из ордена Рук Тени!')
            return HttpResponseRedirect(reverse('sith_page', kwargs={'sith_id': kwargs.get('sith_id')}))
