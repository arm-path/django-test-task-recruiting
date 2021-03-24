from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView, ListView
from django.views.generic.base import View

from django_applications.forms import RecruitForm, SithChoicesForm
from django_applications.models import Recruit, Sith, Test
from django_applications.utils import ValidationTest, DetailMixin


def primary(request):
    """ Представление главной страницы """
    return render(request, 'django_applications/home_page.html', {})


class SithFormView(FormView):
    """ Представление формы выбора ситхов """
    model = Sith
    sith_id = None
    form_class = SithChoicesForm
    template_name = 'django_applications/sith.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ситх'
        return context

    def form_valid(self, form):
        self.sith_id = form.cleaned_data.get('sith').pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('sith_page', kwargs={'sith_id': self.sith_id})


class SithRecruitListView(DetailMixin, View):
    """ Представление формы списка рекрутов для ситха """
    model = Sith
    template = 'django_applications/sith_page_recruits.html'
    template_recruit = 'django_applications/sith_page_recruit.html'


class SithListView(ListView):
    """ Представление списка ситхов """
    model = Sith
    template_name = 'django_applications/siths.html'
    context_object_name = 'siths'

    def get_queryset(self):
        return Sith.objects.annotate(cnt=Count('recruits'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список ситхов'
        return context


class RecruitCreateView(CreateView):
    """ Представление страницы добавления рекрута """
    model = Recruit
    form_class = RecruitForm
    template_name = 'django_applications/recruit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Рекрут'
        return context

    def get_success_url(self):
        return reverse_lazy('test', args=(self.object.pk, self.object.orden_code,))


class TestDetailView(ValidationTest, DetailView):
    """ Представление формы тестов """
    model = Test
    template_name = 'django_applications/test.html'
    slug_url_kwarg = 'orden_code'
    slug_field = 'orden_code'
