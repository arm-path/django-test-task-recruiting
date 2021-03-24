from django.db import models


class Planet(models.Model):
    """ Модель Планет """
    title = models.CharField('Планета', max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Планета'
        verbose_name_plural = 'Планеты'
        ordering = ['title', ]


class Sith(models.Model):
    """ Модель Ситхов """
    name = models.CharField('Имя', max_length=255)
    planet = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, verbose_name='Планета обучения')
    recruits = models.ManyToManyField('Recruit', verbose_name='Рекркты', blank=True)

    def __str__(self):
        return f'{self.name} | {self.planet}'

    class Meta:
        verbose_name = 'Ситх'
        verbose_name_plural = 'Ситхи'


class Recruit(models.Model):
    """ Модель Рекрутов """
    name = models.CharField('Имя', max_length=255)
    planet = models.ForeignKey(Planet, on_delete=models.SET_NULL, null=True, verbose_name='Планета обитания')
    age = models.PositiveSmallIntegerField('Возраст')
    email = models.EmailField('Электронная почта', max_length=50, unique=True)
    orden_code = models.ForeignKey('Test', on_delete=models.PROTECT, verbose_name='Код ордена')
    trials = models.JSONField('Испытание', null=True, blank=True)
    enrolled = models.BooleanField('Зачислен', default=False)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'Рекрут'
        verbose_name_plural = 'Рекруты'


class Questions(models.Model):
    """ Модель вопросов и ответов """
    title = models.CharField('Вопрос', max_length=255, unique=True)
    answer = models.BooleanField('Правильный ответ (ДА | НЕТ)', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Test(models.Model):
    """ Модель тестов """
    orden_code = models.SlugField('Код ордена', max_length=8, unique=True)
    question = models.ManyToManyField(Questions, verbose_name='Список вопросов')

    def __str__(self):
        return self.orden_code

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
