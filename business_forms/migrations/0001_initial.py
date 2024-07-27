# Generated by Django 4.2.13 on 2024-07-27 17:50

import business_forms.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedblogersPreEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Отметка времени')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='ФИ')),
                ('email', models.EmailField(max_length=254, verbose_name='Адрес электронной почты')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('tg_username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ваш Telegram (не канал, а личный никнейм, через @)')),
                ('instagram_username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ваш Instagram')),
                ('policy_agreement', models.BooleanField(default=False, verbose_name='Согласен с политикой обработки персональных данных')),
                ('status', models.IntegerField(choices=[(1, 'Открыт'), (2, 'В клубе'), (3, 'Связалась, жду ответ'), (4, 'Не отвечает'), (5, 'Зайдет позже')], default=1, verbose_name='Статус')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Комментарий менеджера')),
            ],
            options={
                'verbose_name': 'запись в анкете предзаписи в клуб',
                'verbose_name_plural': 'Анкета предзаписи в клуб',
            },
            bases=(models.Model, business_forms.models.BaseModelForm),
        ),
        migrations.CreateModel(
            name='NastavnichestvoPreEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Отметка времени')),
                ('status', models.IntegerField(choices=[(1, 'Открыт'), (2, 'В клубе'), (3, 'Связалась, жду ответ'), (4, 'Не отвечает'), (5, 'Зайдет позже')], default=1, verbose_name='Статус')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='ФИ')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Город проживания в настоящий момент')),
                ('speciality', models.CharField(blank=True, max_length=255, null=True, verbose_name='Специализация (гинеколог, невролог и т.д.)')),
                ('instagram_username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ваш Instagram')),
                ('tg_username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ваш Telegram (не канал, а личный никнейм, через @)')),
                ('target', models.TextField(blank=True, null=True, verbose_name='Какие цели ведения вашего блога?')),
                ('opinion', models.TextField(blank=True, null=True, verbose_name='Как думаете, почему всё ещё их не достигли? Что вас останавливает?')),
                ('results', models.TextField(blank=True, null=True, verbose_name='Каких результатов вы хотите добиться от моего наставничества за данный период (1-2 месяца)?')),
                ('employment_level', models.IntegerField(blank=True, null=True, verbose_name='Оцените уровень вашей занятости от 0 до 10')),
                ('focus', models.TextField(blank=True, null=True, verbose_name='Вы готовы на время наставничества больше сфокусироваться на блоге, чем раньше и, возможно, отложить другие дела (помимо работы, естесна)?')),
                ('questions', models.TextField(blank=True, null=True, verbose_name='Наверное у вас остались вопросы? С радостью отвечу на них на созвоне)')),
                ('email', models.EmailField(max_length=254, verbose_name='Адрес электронной почты')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('price', models.TextField(blank=True, null=True, verbose_name='И главный вопрос (от вас ко мне) - сколько стоит? Можете написать свой вариант, а я на созвоне скажу, насколько вы точно попали))')),
                ('need_nmo', models.TextField(blank=True, null=True, verbose_name='Вам нужно 144 балла НМО, как за прохождение ИнстаТерапии? (это за доп.плату) 😁')),
            ],
            options={
                'verbose_name': 'запись в анкете предзаписи на наставничество',
                'verbose_name_plural': 'Анкета предзаписи на наставничество',
            },
        ),
        migrations.CreateModel(
            name='BusinessForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('photo', models.ImageField(upload_to=business_forms.models.BusinessForm.get_upload_photo_path)),
                ('spasibo_photo', models.ImageField(upload_to=business_forms.models.BusinessForm.get_upload_spasibo_path)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Конфигурации форм',
                'verbose_name_plural': 'Конфигурации форм',
            },
        ),
    ]
