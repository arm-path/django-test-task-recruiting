from django.contrib import admin

from .models import Planet, Sith, Recruit, Questions, Test


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    """ Представление Планет в административной панели """
    pass


@admin.register(Sith)
class SithAdmin(admin.ModelAdmin):
    """ Представление Ситхов в административной панели """
    list_display = ['name', 'planet', 'get_count_recruits']
    list_filter = ['planet']
    search_fields = ['name']

    def get_count_recruits(self, obj):
        """ Количество рекрутов """
        if obj.recruits:
            return obj.recruits.count()

    get_count_recruits.short_description = "Количество рекрутов"


@admin.register(Recruit)
class RecruitAdmin(admin.ModelAdmin):
    """ Представление Рекрутов в административной панели """
    list_display = ['name', 'planet', 'email', 'enrolled']
    list_filter = ['planet', 'enrolled']
    search_fields = ['name', 'email']

    # list_editable = ['enrolled']


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    """ Представление Вопросов в административной панели """
    list_display = ['title', 'answer']
    search_fields = ['title']


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """ Представление тестов в административной панели """
    pass
