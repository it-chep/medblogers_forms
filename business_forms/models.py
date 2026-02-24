import os
import re

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import SuspiciousFileOperation
from django.db import models
from django.utils.html import format_html
from business_forms.utils import format_phone_number

ZERO_TO_TEN_CHOICES = (
    ("0", "0"),
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
)

ONE_TO_TEN_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
)


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
        if self.instagram_username is None:
            return ""
        return f"https://instagram.com/{self.instagram_username}"

    @property
    def tg_username_link(self):
        if self.tg_username is None:
            return ""
        tg_username = self.tg_username.replace("@", '')
        return f"https://t.me/{tg_username}"

    @property
    def wa_link(self):
        if self.phone is None or len(self.phone) == 0:
            return ""
        return f"https://wa.me/{self.phone}"

    @property
    def tg_phone_link(self):
        if self.phone is None or len(self.phone) == 0:
            return ""
        return f"https://t.me/{format_phone_number(self.phone)}"

    def formatted_instagram_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.instagram_link, 'Посмотреть Instagram')

    def formatted_tg_username_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.tg_username_link, 'Написать человеку')

    def formatted_tg_phone_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.tg_phone_link, 'Написать человеку')

    def formatted_wa_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.wa_link, 'Написать человеку')

    formatted_wa_link.short_description = 'Ссылка на Whatsapp'
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


class ExpressMedbloger(models.Model, BaseModelForm):
    AVERAGE_INCOME_CHOICES = (
        ("0-50", "до 50тыс"),
        ("50-100", "50 - 100тыс"),
        ("100-150", "100 - 150тыс"),
        ("150-200", "150 - 200тыс"),
        ("200-300", "200 - 300тыс"),
        ("300-500", "300 - 500тыс"),
        ("500-1кк", "500тыс - 1млн"),
        ("1кк+", "1млн+"),
    )

    MARKETING_TYPE_CHOICES = (
        ("instagram", "Instagram"),
        ("telegram", "Telegram"),
        ("bot", "Рассылка в боте"),
        ("email", "Рассылка на почте"),
        ("meducation", "Блог Meducation"),
    )

    MEDBLOG_CHOICES = (
        ("yes_money", "Веду, получаю с него стабильный доход"),
        ("yes_no_money", "Веду, но не очень результативно / не зарабатываю с него"),
        ("no", "Не веду, только планирую завести"),
    )

    marketing_type = models.CharField(
        max_length=255, choices=MARKETING_TYPE_CHOICES,
        verbose_name="Я увидел(а) эту анкету в:",
        null=True, blank=True
    )
    have_bought_products = models.CharField(
        max_length=255,
        verbose_name="Вы покупали какие-то мои продукты?",
        null=True, blank=True
    )
    speciality = models.CharField(
        max_length=255, verbose_name="Специализация (гинеколог, невролог и т.д.)",
        blank=True, null=True
    )
    average_income = models.CharField(
        max_length=255, choices=AVERAGE_INCOME_CHOICES,
        verbose_name="Ваш средний доход в месяц, в рублях, суммарный со всех источников",
        null=True, blank=True
    )
    medblog = models.CharField(
        max_length=255, choices=MEDBLOG_CHOICES,
        verbose_name="Медблог:",
        null=True, blank=True
    )
    medblog_reason = models.TextField(
        verbose_name="Зачем вы ведёте / хотите вести медблог?",
        null=True, blank=True,
    )
    medblog_complexity = models.TextField(
        verbose_name="Какие сложности есть сейчас с блогом? Что останавливает от того, чтобы достичь целей выше?",
        null=True, blank=True,
    )
    medblog_helped = models.TextField(
        verbose_name="Что уже пробовали делать, чтобы решить проблему? Что помогло, а что - не очень?",
        null=True, blank=True,
    )
    how_long_following = models.TextField(
        verbose_name="Как давно вы на меня подписаны и откуда узнали?",
        null=True, blank=True,
    )
    top_questions = models.TextField(
        verbose_name="ТОП-1 или ТОП-3 вопроса по блогингу, которые вы хотите решить прямо сейчас:",
        null=True, blank=True,
    )
    how_warmed_up = models.CharField(
        max_length=255, choices=ZERO_TO_TEN_CHOICES,
        verbose_name="На сколько от 0 до 10 вы прогреты, чтобы начать у меня обучение любого формата?",
        null=True, blank=True,
    )
    rate_of_employment = models.CharField(
        max_length=255, choices=ZERO_TO_TEN_CHOICES,
        verbose_name="Оцените уровень вашей занятости от 0 до 10",
        null=True, blank=True,
    )
    name = models.CharField(
        max_length=255, verbose_name="Ваше ФИО",
        null=True, blank=True
    )
    age = models.CharField(
        max_length=255, verbose_name="Возраст",
        blank=True, null=True
    )
    city = models.CharField(
        max_length=255, verbose_name="Город проживания в настоящий момент",
        blank=True, null=True
    )
    instagram_username = models.CharField(
        max_length=255, verbose_name="Ссылка на ваш инстаграм",
        null=True, blank=True
    )
    tg_channel_url = models.CharField(
        max_length=255, verbose_name="Ссылка на ваш телеграм-канал",
        null=True, blank=True
    )
    tg_username = models.CharField(
        max_length=255,
        verbose_name="Ссылка на ваш личный телеграм (не канал) в формате https://t.me/readydoc или через @",
        null=True, blank=True
    )
    phone = models.CharField(
        max_length=255, verbose_name="Контактный телефон", null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты", null=True, blank=True
    )

    policy_agreement = models.BooleanField(
        verbose_name="Согласен с политикой обработки персональных данных",
        default=False
    )

    def __str__(self):
        return f"Анкета 'Экспресс-разбор медблога': {self.name}"

    class Meta:
        verbose_name = "запись в анкете 'Экспресс-разбор медблога'"
        verbose_name_plural = "Анкета 'Экспресс-разбор медблога'"


class NeuroMedbloger(models.Model, BaseModelForm):
    name = models.CharField(
        max_length=255, verbose_name="Ваше ФИО",
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
    phone = models.CharField(
        max_length=255, verbose_name="Контактный телефон", null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты", null=True, blank=True
    )
    tg_username = models.CharField(
        max_length=255,
        verbose_name="Ссылка на ваш личный телеграм (не канал) в формате https://t.me/readydoc или через @",
        null=True, blank=True
    )
    level_of_use_neuro = models.CharField(
        max_length=255, choices=ZERO_TO_TEN_CHOICES,
        verbose_name="Оцените уровень вашего пользования нейросетями для создания контента",
        null=True, blank=True,
    )
    your_questions = models.TextField(
        verbose_name="Ваши вопросы",
        null=True, blank=True,
    )

    policy_agreement = models.BooleanField(
        verbose_name="Согласен с политикой обработки персональных данных",
        default=False
    )

    def __str__(self):
        return f"Анкета 'Нейросети для медблога': {self.name}"

    class Meta:
        verbose_name = "запись в анкете 'Нейросети для медблога'"
        verbose_name_plural = "Анкета 'Нейросети для медблога'"


class SMMSpecialists(models.Model):
    LAST_COLLABORATION_PERIOD_CHOICES = (
        ("3_month", "До 3 месяцев"),
        ("3_6_month", "3-6 месяцев"),
        ("1_year", "До года"),
        ("More_1_year", "Более года"),
    )

    SATISFIED_OF_RESULT_CHOICES = (
        ("all_good", "Всё было отлично, сотрудничество помогло решить задачи"),
        ("50_50", "В целом неплохо, но есть нюансы"),
        ("bad_exp", "Нет, ожидания не оправдались"),
    )

    SOCIAL_NETWORKS_CHOICES = (
        ("Instagram", "Instagram"),
        ("Telegram", "Telegram"),
        ("VK", "VK"),
        ("YouTube", "YouTube"),
    )

    YOUR_EXPERIENCE_CHOICES = (
        ("yes_smm", "Да, СММ"),
        ("yes_advertising_manager", "Да, менеджер по рекламе"),
        ("yes_producer", "Да, продюсер"),
        ("yes_designer", "Да, дизайнер"),
        ("yes_marketolog", "Да, маркетолог"),
        ("no_but_planning", "Нет, но думаю об этом"),
        ("no_no_planning", "Нет и не планирую"),
    )

    SOCIAL_NETWORKS_MAPPING = {
        "Instagram": "Instagram",
        "Telegram": "Telegram",
        "VK": "VK",
        "YouTube": "YouTube",
    }

    YOUR_EXPERIENCE_MAPPING = {
        "yes_smm": "Да, СММ",
        "yes_advertising_manager": "Да, менеджер по рекламе",
        "yes_producer": "Да, продюсер",
        "yes_designer": "Да, дизайнер",
        "yes_marketolog": "Да, маркетолог",
        "no_but_planning": "Нет, но думаю об этом",
        "no_no_planning": "Нет и не планирую",
    }

    specialization = models.CharField(
        verbose_name="Ваша специализация", max_length=255,
        null=True, blank=True,
    )

    # множественный выбор
    social_networks = models.CharField(
        verbose_name="В каких соцсетях вы ведёте блог?",
        max_length=255,
        null=True, blank=True,
    )

    # множественный выбор
    your_experience = models.CharField(
        verbose_name="Обращались ли вы за помощью к digital специалистам? (если нужной профессии нет в списке, напишите в последней строке)",
        max_length=500,
        db_column='your_experience',
        null=True, blank=True,
    )

    last_collaboration_period = models.CharField(
        verbose_name="Сколько продлилось ваше сотрудничество?",
        max_length=255,
        choices=LAST_COLLABORATION_PERIOD_CHOICES,
        db_column='last_collaboration_period',
        null=True, blank=True,
    )

    satisfied_of_results = models.CharField(
        verbose_name="Довольны ли результатами?",
        max_length=255,
        choices=SATISFIED_OF_RESULT_CHOICES,
        db_column='satisfied_of_results',
        null=True, blank=True,
    )

    positive_specialist_contact = models.CharField(
        verbose_name="Оставьте контакт на своего digital специалиста, если готовы его рекомендовать", max_length=500,
        db_column='positive_specialist_contact',
        null=True, blank=True,
    )

    negative_specialist_contact = models.CharField(
        verbose_name="А в этом окне оставьте контакт digital специалиста, с которым НЕ рекомендуете сотрудничать",
        max_length=500,
        db_column='neg_specialist_contact',
        null=True, blank=True,
    )

    user_contact = models.CharField(
        verbose_name="Если вы готовы пообщаться с нами подробнее на тему СММ и подбора проверенных подрядчиков, оставьте свой телеграм через @ или ссылкой",
        max_length=255,
        db_column='user_contact',
        null=True, blank=True,
    )

    def __str__(self):
        return f"Анкета 'рекомендации SMM специалиста'"

    class Meta:
        verbose_name = "запись в анкете 'рекомендации SMM специалиста'"
        verbose_name_plural = "Анкета 'рекомендации SMM специалиста'"

    @property
    def tg_username_link(self):
        tg_username = self.user_contact.replace("@", '')
        return f"https://t.me/{tg_username}"

    def formatted_user_contact(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.tg_username_link, 'Написать человеку')


class Speecadoc(models.Model, BaseModelForm):
    AVERAGE_INCOME_CHOICES = (
        ("0-50", "до 50тыс"),
        ("50-100", "50 - 100тыс"),
        ("100-150", "100 - 150тыс"),
        ("150-200", "150 - 200тыс"),
        ("200-300", "200 - 300тыс"),
        ("300-500", "300 - 500тыс"),
        ("500-1кк", "500тыс - 1млн"),
        ("1кк+", "1млн+"),
    )

    MARKETING_TYPE_CHOICES = (
        ("instagram", "Instagram"),
        ("telegram", "Telegram"),
        ("bot", "Рассылка в боте"),
        ("email", "Рассылка на почте"),
        ("meducation", "Блог Meducation"),
    )

    MEDBLOG_CHOICES = (
        ("yes_money", "Веду, получаю с него стабильный доход"),
        ("yes_no_money", "Веду, но не очень результативно / не зарабатываю с него"),
        ("no", "Не веду, только планирую завести"),
    )

    marketing_type = models.CharField(
        max_length=255, choices=MARKETING_TYPE_CHOICES,
        verbose_name="Я увидел(а) эту анкету в:",
        null=True, blank=True
    )
    have_bought_products = models.CharField(
        max_length=255,
        verbose_name="Вы покупали какие-то мои продукты?",
        null=True, blank=True
    )
    speciality = models.CharField(
        max_length=255, verbose_name="Специализация (гинеколог, невролог и т.д.)",
        blank=True, null=True
    )
    average_income = models.CharField(
        max_length=255, choices=AVERAGE_INCOME_CHOICES,
        verbose_name="Ваш средний доход в месяц, в рублях, суммарный со всех источников",
        null=True, blank=True
    )
    medblog = models.CharField(
        max_length=255, choices=MEDBLOG_CHOICES,
        verbose_name="Медблог:",
        null=True, blank=True
    )
    medblog_reason = models.TextField(
        verbose_name="Зачем вы ведёте / хотите вести медблог?",
        null=True, blank=True,
    )
    medblog_complexity = models.TextField(
        verbose_name="Какие сложности есть сейчас с блогом? Что останавливает от того, чтобы достичь целей выше?",
        null=True, blank=True,
    )
    medblog_helped = models.TextField(
        verbose_name="Что уже пробовали делать, чтобы решить проблему? Что помогло, а что - не очень?",
        null=True, blank=True,
    )
    how_long_following = models.TextField(
        verbose_name="Как давно вы на меня подписаны и откуда узнали?",
        null=True, blank=True,
    )
    top_questions = models.TextField(
        verbose_name="ТОП-1 или ТОП-3 вопроса по блогингу, которые вы хотите решить прямо сейчас:",
        null=True, blank=True,
    )
    how_warmed_up = models.CharField(
        max_length=255, choices=ZERO_TO_TEN_CHOICES,
        verbose_name="На сколько от 0 до 10 вы прогреты, чтобы начать у меня обучение любого формата?",
        null=True, blank=True,
    )
    rate_of_employment = models.CharField(
        max_length=255, choices=ZERO_TO_TEN_CHOICES,
        verbose_name="Оцените уровень вашей занятости от 0 до 10",
        null=True, blank=True,
    )
    name = models.CharField(
        max_length=255, verbose_name="Ваше ФИО",
        null=True, blank=True
    )
    age = models.CharField(
        max_length=255, verbose_name="Возраст",
        blank=True, null=True
    )
    city = models.CharField(
        max_length=255, verbose_name="Город проживания в настоящий момент",
        blank=True, null=True
    )
    instagram_username = models.CharField(
        max_length=255, verbose_name="Ссылка на ваш инстаграм",
        null=True, blank=True
    )
    tg_channel_url = models.CharField(
        max_length=255, verbose_name="Ссылка на ваш телеграм-канал",
        null=True, blank=True
    )
    tg_username = models.CharField(
        max_length=255,
        verbose_name="Ссылка на ваш личный телеграм (не канал) в формате https://t.me/readydoc или через @",
        null=True, blank=True
    )
    phone = models.CharField(
        max_length=255, verbose_name="Контактный телефон", null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты", null=True, blank=True
    )

    policy_agreement = models.BooleanField(
        verbose_name="Согласен с политикой обработки персональных данных",
        default=False
    )

    def __str__(self):
        return f"Анкета 'Настав кати': {self.name}"

    class Meta:
        verbose_name = "запись в анкете 'Настав кати'"
        verbose_name_plural = "Анкета 'Настав кати'"


class MedSMM(models.Model, BaseModelForm):
    MARKETING_TYPE_CHOICES = (
        ("instagram", "Instagram"),
        ("telegram", "Telegram"),
        ("bot", "Рассылка в боте"),
        ("email", "Рассылка на почте"),
    )

    AGE_RANGE_CHOICES = (
        ("18-", "до 18"),
        ("18-24", "18-24"),
        ("25-30", "25-30"),
        ("31-35", "31-35"),
        ("36-40", "36-40"),
        ("41-45", "41-45"),
        ("46-51", "46-51"),
        ("52+", "52+"),
    )

    AVERAGE_INCOME_CHOICES = (
        ("0-50", "до 50 тыс"),
        ("50-100", "50 - 100 тыс"),
        ("100-150", "100 - 150 тыс"),
        ("150-200", "150 - 200 тыс"),
        ("200-300", "200 - 300 тыс"),
        ("300-500", "300 - 500 тыс"),
        ("500+", "свыше 500 тыс"),
    )

    TRIED_BLOGGING_CHOICES = (
        ("personal", "Да, но только личный"),
        ("expert", "Да, пробовал вести / веду свой экспертный"),
        ("other_person", "Да, но не себе, а кому-то другому"),
        ("never", "Ни разу не вёл"),
    )

    SMM_EDUCATION_CHOICES = (
        ("paid", "Да, проходил платные курсы"),
        ("free", "Да, но смотрел только бесплатные материалы (инста, ютуб и тд)"),
        ("none", "Не обучался"),
    )

    SKILLS_CHOICES = (
        ("blog_packaging", "Упаковывать блог (шапка, хайлайтс и тд)"),
        ("content_ideas", "Придумывать идеи для контента"),
        ("copywriting", "Писать тексты постов"),
        ("video", "Снимать / монтировать видео"),
        ("design", "Дизайнить (Canva, Photoshop и тд)"),
        ("web_development", "Верстать сайты / таплинк"),
        ("neural_networks", "Работать с нейросетями"),
        ("client_search", "Находить клиентов"),
        ("sales", "Продавать"),
        ("spreadsheets", "Вести таблицы / планнеры / составлять презентации"),
        ("documents", "Составлять юридические документы (договор, акт и тд)"),
    )

    SKILLS_MAPPING = {
        "blog_packaging": "Упаковывать блог (шапка, хайлайтс и тд)",
        "content_ideas": "Придумывать идеи для контента",
        "copywriting": "Писать тексты постов",
        "video": "Снимать / монтировать видео",
        "design": "Дизайнить (Canva, Photoshop и тд)",
        "web_development": "Верстать сайты / таплинк",
        "neural_networks": "Работать с нейросетями",
        "client_search": "Находить клиентов",
        "sales": "Продавать",
        "spreadsheets": "Вести таблицы / планнеры / составлять презентации",
        "documents": "Составлять юридические документы (договор, акт и тд)",
    }

    OCCUPATION_CHOICES = (
        ("student", "Студент меда"),
        ("ordinatur", "Ординатор"),
        ("doctor", "Работаю врачом"),
        ("smm_worker", "Работаю в SMM"),
        ("maternity", "Декрет"),
    )

    OCCUPATION_MAPPING = {
        "student": "Студент меда",
        "ordinatur": "Ординатор",
        "doctor": "Работаю врачом",
        "smm_worker": "Работаю в SMM",
        "maternity": "Декрет",
    }

    DESIRED_INCOME_CHOICES = (
        ("20-30", "20 - 30 тыс"),
        ("30-60", "30 - 60 тыс"),
        ("60-100", "60 - 100 тыс"),
        ("100+", "100 тыс+"),
    )

    INVESTMENT_READINESS_CHOICES = (
        ("20-30", "20 - 30 тыс"),
        ("30-50", "30 - 50 тыс"),
        ("50-100", "50 - 100 тыс"),
        ("100+", "100+ тыс"),
    )

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Отметка времени", null=True, blank=True)

    marketing_type = models.CharField(
        max_length=255, choices=MARKETING_TYPE_CHOICES,
        verbose_name="Вы увидели эту анкету у меня в:",
        null=True, blank=True
    )
    age_range = models.CharField(
        max_length=255, choices=AGE_RANGE_CHOICES,
        verbose_name="Ваш возраст",
        null=True, blank=True
    )
    occupation = models.CharField(
        max_length=255,
        verbose_name="Чем вы сейчас занимаетесь? (род деятельности)",
        null=True, blank=True
    )
    average_income = models.CharField(
        max_length=255, choices=AVERAGE_INCOME_CHOICES,
        verbose_name="Ваш средний доход в месяц, в рублях (суммарный со всех источников)",
        null=True, blank=True
    )
    reason_for_career_change = models.TextField(
        verbose_name="Почему задумываетесь о смене профессии?",
        null=True, blank=True,
    )
    disappointment_level = models.CharField(
        max_length=255, choices=ONE_TO_TEN_CHOICES,
        verbose_name="Оцените уровень разочарования в профессии врача от 0 до 10",
        null=True, blank=True,
    )
    tried_blogging = models.CharField(
        max_length=255, choices=TRIED_BLOGGING_CHOICES,
        verbose_name="Вы пробовали вести блог? (в любой соцсети)",
        null=True, blank=True
    )
    smm_education = models.CharField(
        max_length=255, choices=SMM_EDUCATION_CHOICES,
        verbose_name="Вы уже обучались где-то SMM / маркетингу / блогингу?",
        null=True, blank=True
    )
    skills = models.CharField(
        verbose_name="Что умеете делать?",
        max_length=500,
        null=True, blank=True,
    )
    smm_work_vision = models.TextField(
        verbose_name="Как вы представляете работу SMM-специалиста?",
        null=True, blank=True,
    )
    desired_income = models.CharField(
        max_length=255, choices=DESIRED_INCOME_CHOICES,
        verbose_name="Какой доход в SMM через 6 месяцев был бы для вас успехом (в месяц в рублях)",
        null=True, blank=True
    )
    top_fears = models.TextField(
        verbose_name="Что для вас самое страшное в работе SMM на текущий момент? ТОП-3 страха",
        null=True, blank=True,
    )
    investment_readiness = models.CharField(
        max_length=255, choices=INVESTMENT_READINESS_CHOICES,
        verbose_name="Сколько готовы вложить в освоение новой профессии SMM?",
        null=True, blank=True
    )
    five_year_plan = models.TextField(
        verbose_name="Кем и где вы хотите работать через 5 лет и сколько зарабатывать?",
        null=True, blank=True,
    )
    name = models.CharField(
        max_length=255, verbose_name="Ваши Имя и Фамилия",
        null=True, blank=True
    )
    city = models.CharField(
        max_length=255, verbose_name="Город проживания в настоящий момент",
        null=True, blank=True
    )
    instagram_username = models.CharField(
        max_length=255, verbose_name="Ссылка на ваш инстаграм",
        null=True, blank=True
    )
    tg_username = models.CharField(
        max_length=255,
        verbose_name="Ссылка на ваш личный телеграм (не канал) в формате https://t.me/readydoc или через @",
        null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Email", null=True, blank=True
    )
    phone = models.CharField(
        max_length=255, verbose_name="Номер телефона через +7", null=True, blank=True
    )

    policy_agreement = models.BooleanField(
        verbose_name="Даю согласие на обработку персональных данных",
        default=False
    )

    def __str__(self):
        return f"Анкета 'МЕД SMM-специалистов': {self.name}"

    class Meta:
        verbose_name = "запись в анкете 'МЕД SMM-специалистов'"
        verbose_name_plural = "Анкета 'МЕД SMM-специалистов'"
