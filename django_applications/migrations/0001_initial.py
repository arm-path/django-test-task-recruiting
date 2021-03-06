# Generated by Django 3.1.7 on 2021-03-22 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Планета')),
            ],
            options={
                'verbose_name': 'Планета',
                'verbose_name_plural': 'Планеты',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Вопрос')),
                ('answer', models.BooleanField(default=False, verbose_name='Правильный ответ (ДА | НЕТ)')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden_code', models.IntegerField(unique=True, verbose_name='Код ордена')),
                ('question', models.ManyToManyField(to='django_applications.Questions', verbose_name='Список вопросов')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.CreateModel(
            name='Sith',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('planet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_applications.planet', verbose_name='Планета обучения')),
            ],
            options={
                'verbose_name': 'Ситх',
                'verbose_name_plural': 'Ситхи',
            },
        ),
        migrations.CreateModel(
            name='Recruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('age', models.PositiveSmallIntegerField(verbose_name='Возраст')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Электронная почта')),
                ('planet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_applications.planet', verbose_name='Планета обитания')),
            ],
            options={
                'verbose_name': 'Рекрут',
                'verbose_name_plural': 'Рекруты',
            },
        ),
    ]
