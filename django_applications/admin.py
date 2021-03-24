from django.contrib import admin

from .models import Planet, Sith, Recruit, Questions, Test


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    """ Представление Планет в административной панели """
    pass


@admin.register(Sith)
class PlanetAdmin(admin.ModelAdmin):
    """ Представление Планет в административной панели """
    pass


@admin.register(Recruit)
class PlanetAdmin(admin.ModelAdmin):
    """ Представление Планет в административной панели """
    pass


@admin.register(Questions)
class PlanetAdmin(admin.ModelAdmin):
    """ Представление Планет в административной панели """
    pass


@admin.register(Test)
class PlanetAdmin(admin.ModelAdmin):
    """ Представление Планет в административной панели """
    pass
