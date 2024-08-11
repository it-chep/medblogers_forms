import os
import re

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import SuspiciousFileOperation
from django.db import models
from django.utils.html import format_html
from business_forms.utils import format_phone_number


def safe_filename(filename):
    filename = re.sub(r'[^\w\s.-]', '', filename).strip()
    if '..' in filename or filename.startswith('/'):
        raise SuspiciousFileOperation("Detected path traversal attempt")
    return filename


class BusinessForm(models.Model):
    def get_upload_photo_path(self, filename):
        filename = safe_filename(filename)
        return os.path.join('banners', filename)

    def get_upload_spasibo_path(self, filename):
        filename = safe_filename(filename)
        return os.path.join('spasibo', filename)

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    photo = models.ImageField(upload_to=get_upload_photo_path)
    spasibo_photo = models.ImageField(upload_to=get_upload_spasibo_path)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Конфигурации форм"
        verbose_name_plural = "Конфигурации форм"


class BaseModelForm:

    @property
    def instagram_link(self):
        return f"https://instagram.com/{self.instagram_username}"

    @property
    def tg_username_link(self):
        tg_username = self.tg_username.replace("@", '')
        return f"https://t.me/{tg_username}"

    @property
    def tg_phone_link(self):
        return f"https://t.me/{format_phone_number(self.phone)}"

    def formatted_instagram_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.instagram_link, 'Посмотреть Instagram')

    def formatted_tg_username_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.tg_username_link, 'Написать человеку')

    def formatted_tg_phone_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.tg_phone_link, 'Написать человеку')

    formatted_instagram_link.short_description = 'Ссылка на instagram'
    formatted_tg_username_link.short_description = 'Ссылка TG сформированная по никнейму'
    formatted_tg_phone_link.short_description = 'Ссылка TG сформированная по номеру телефона'


class MedblogersPreEntry(models.Model, BaseModelForm):
    PRE_ENTRY_CHOICES = (
        (1, "Открыт"),
        (2, "В клубе"),
        (3, "Связалась, жду ответ"),
        (4, "Не отвечает"),
        (5, "Зайдет позже")
    )

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Отметка времени", null=True, blank=True)
    name = models.CharField(
        max_length=255, verbose_name="ФИ",
        null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
    )
    phone = models.CharField(
        max_length=20, verbose_name="Номер телефона",
        null=True, blank=True
    )

    tg_username = models.CharField(
        max_length=255, verbose_name="Ваш Telegram (не канал, а личный никнейм, через @)",
        null=True, blank=True
    )

    instagram_username = models.CharField(
        max_length=255, verbose_name="Ваш Instagram",
        null=True, blank=True
    )

    policy_agreement = models.BooleanField(
        verbose_name="Согласен с политикой обработки персональных данных",
        default=False
    )

    status = models.IntegerField(choices=PRE_ENTRY_CHOICES, default=1, verbose_name="Статус")

    description = models.TextField(verbose_name="Комментарий менеджера", null=True, blank=True)

    def colored_status(self):
        color = 'black'
        background_color = 'white'
        if self.status == 2:
            color = 'white'
            background_color = '#4dab4d'
        elif self.status == 3:
            color = 'white'
            background_color = '#ff9c00'
        elif self.status == 4:
            color = 'white'
            background_color = '#ff0000'
        elif self.status == 5:
            color = 'white'
            background_color = 'black'
        return format_html(
            '<span style="background-color: {}; color: {}; border: 1px solid black; position:relative; display: '
            'block; padding: 5px; text-align: center;'
            'margin: -5px; border-radius: 8px;">{}</span>', background_color, color,
            self.get_status_display()
        )

    colored_status.short_description = 'Статус'

    def __str__(self):
        return f"Анкета клиента клуба: {self.name}"

    class Meta:
        verbose_name = "запись в анкете предзаписи в клуб"
        verbose_name_plural = "Анкета предзаписи в клуб"


class NastavnichestvoPreEntry(models.Model):
    NASTAVNICHESTVO_CHOICES = (
        (1, "Открыт"),
        (2, "В клубе"),
        (3, "Связалась, жду ответ"),
        (4, "Не отвечает"),
        (5, "Зайдет позже")
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Отметка времени")

    status = models.IntegerField(choices=NASTAVNICHESTVO_CHOICES, default=1, verbose_name="Статус")

    name = models.CharField(
        max_length=255, verbose_name="ФИ",
        null=True, blank=True
    )
    city = models.CharField(
        max_length=255, verbose_name="Город проживания в настоящий момент",
        blank=True, null=True
    )
    speciality = models.CharField(
        max_length=255, verbose_name="Специализация (гинеколог, невролог и т.д.)",
        blank=True, null=True
    )
    instagram_username = models.CharField(
        max_length=255, verbose_name="Ваш Instagram",
        null=True, blank=True
    )
    tg_username = models.CharField(
        max_length=255, verbose_name="Ваш Telegram (не канал, а личный никнейм, через @)",
        null=True, blank=True
    )
    target = models.TextField(
        verbose_name="Какие цели ведения вашего блога?",
        null=True, blank=True
    )
    opinion = models.TextField(
        verbose_name="Как думаете, почему всё ещё их не достигли? Что вас останавливает?",
        null=True, blank=True
    )
    results = models.TextField(
        verbose_name="Каких результатов вы хотите добиться от моего наставничества за данный период (1-2 месяца)?",
        null=True, blank=True
    )
    employment_level = models.IntegerField(
        verbose_name="Оцените уровень вашей занятости от 0 до 10",
        null=True, blank=True
    )
    focus = models.TextField(
        verbose_name="Вы готовы на время наставничества больше сфокусироваться на блоге, чем раньше и, возможно, отложить другие дела (помимо работы, естесна)?",
        null=True, blank=True
    )
    questions = models.TextField(
        verbose_name="Наверное у вас остались вопросы? С радостью отвечу на них на созвоне)",
        null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты"
    )
    phone = models.CharField(
        max_length=20, verbose_name="Номер телефона",
        null=True, blank=True
    )
    price = models.TextField(
        verbose_name="И главный вопрос (от вас ко мне) - сколько стоит? Можете написать свой вариант, а я на созвоне скажу, насколько вы точно попали))",
        null=True, blank=True
    )
    need_nmo = models.TextField(
        verbose_name="Вам нужно 144 балла НМО, как за прохождение ИнстаТерапии? (это за доп.плату) 😁",
        null=True, blank=True
    )

    @property
    def tg_link(self):
        if self.tg_username:
            tg_username = self.tg_username.replace('@', '')
            return f"https://t.me/{tg_username}"
        else:
            return f"https://t.me/{format_phone_number(self.phone)}"

    def colored_status(self):
        color = 'black'
        background_color = 'white'
        if self.status == 2:
            color = 'white'
            background_color = '#4dab4d'
        elif self.status == 3:
            color = 'white'
            background_color = '#ff9c00'
        elif self.status == 4:
            color = 'white'
            background_color = '#ff0000'
        elif self.status == 5:
            color = 'white'
            background_color = 'black'
        return format_html(
            '<span style="background-color: {}; color: {}; border: 1px solid black; position:relative; display: '
            'block; padding: 5px; text-align: center;'
            'margin: -5px; border-radius: 8px;">{}</span>', background_color, color,
            self.get_status_display()
        )

    colored_status.short_description = 'Статус'

    class Meta:
        verbose_name = "запись в анкете предзаписи на наставничество"
        verbose_name_plural = "Анкета предзаписи на наставничество"


class NationalBlogersAssociation(models.Model):
    NATIONAL_CHOICES = (
        (1, "Открыт"),
        (2, "В клубе"),
        (3, "Связалась, жду ответ"),
        (4, "Не отвечает"),
        (5, "Зайдет позже")
    )
    status = models.IntegerField(choices=NATIONAL_CHOICES, default=1, verbose_name="Статус")

    name = models.CharField(
        max_length=255, verbose_name="Ваше имя и фамилия", null=True, blank=True
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения", null=True, blank=True
    )
    city = models.CharField(
        max_length=255, verbose_name="Город проживания", null=True, blank=True
    )
    job = models.CharField(
        max_length=255, verbose_name="Место работы, должность", null=True, blank=True
    )
    speciality = models.CharField(
        max_length=255, verbose_name="Специальность", null=True, blank=True
    )
    phone_number = models.CharField(
        max_length=255, verbose_name="Контактный телефон", null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты", null=True, blank=True
    )
    blog_link = models.CharField(
        verbose_name="Ссылка на социальные сети / блог", max_length=255, null=True, blank=True
    )
    expectations = models.TextField(
        verbose_name="Ваши ожидания от участия в Национальной Ассоциации блогеров в сфере здравоохранения", null=True,
        blank=True
    )
    policy_agreement = models.BooleanField(
        verbose_name="Согласен с политикой обработки персональных данных",
        default=False
    )

    def colored_status(self):
        color = 'black'
        background_color = 'white'
        if self.status == 2:
            color = 'white'
            background_color = '#4dab4d'
        elif self.status == 3:
            color = 'white'
            background_color = '#ff9c00'
        elif self.status == 4:
            color = 'white'
            background_color = '#ff0000'
        elif self.status == 5:
            color = 'white'
            background_color = 'black'
        return format_html(
            '<span style="background-color: {}; color: {}; border: 1px solid black; position:relative; display: '
            'block; padding: 5px; text-align: center;'
            'margin: -5px; border-radius: 8px;">{}</span>', background_color, color,
            self.get_status_display()
        )

    colored_status.short_description = 'Статус'

    class Meta:
        verbose_name = "запись в анкете Национальная ассоциация блогеров в сфере здравоохранения"
        verbose_name_plural = "Анкета Национальная ассоциация блогеров в сфере здравоохранения"
