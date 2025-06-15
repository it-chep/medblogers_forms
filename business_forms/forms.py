from django import forms
from business_forms.models import MedblogersPreEntry, NationalBlogersAssociation, ExpressMedbloger,ZERO_TO_TEN_CHOICES


class MedblogersPreEntryForm(forms.ModelForm):
    """Форма предзаписи в клуб"""

    class Meta:
        model = MedblogersPreEntry
        fields = (
            "name",
            "email",
            "phone",
            "instagram_username",
            "tg_username",
            "policy_agreement",
        )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Мой ответ'}, ),
            'phone': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'instagram_username': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'tg_username': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'policy_agreement': forms.CheckboxInput(attrs={'style': 'display:none'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

        self.fields['email'].error_messages.update({
            'invalid': 'Введите правильный адрес электронной почты.'
        })


class NationalBlogersAssociationForm(forms.ModelForm):
    class Meta:
        model = NationalBlogersAssociation
        fields = (
            "name",
            "birth_date",
            "city",
            "job",
            "speciality",
            "phone_number",
            "email",
            "blog_link",
            "expectations",
            "policy_agreement",
        )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'birth_date': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'ДД.ММ.ГГГГ'}),
            'city': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'job': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'speciality': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Мой ответ'}, ),
            'blog_link': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'expectations': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'policy_agreement': forms.CheckboxInput(attrs={'style': 'display:none'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

        self.fields['email'].error_messages.update({
            'invalid': 'Введите правильный адрес электронной почты.'
        })


class ExpressMedblogerForm(forms.ModelForm):
    """Экспресс-разбор медблога"""

    class Meta:
        model = ExpressMedbloger
        fields = (
            "marketing_type",
            "have_bought_products",
            "speciality",
            "average_income",
            "medblog",
            "medblog_reason",
            "medblog_complexity",
            "medblog_helped",
            "how_long_following",
            "top_questions",
            "how_warmed_up",
            "rate_of_employment",
            "name",
            "age",
            "city",
            "instagram_username",
            "tg_channel_url",
            "tg_username",
            "phone",
            "email",
            "policy_agreement",
        )
        widgets = {
            'speciality': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'medblog_reason': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'medblog_complexity': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'medblog_helped': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'how_long_following': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'top_questions': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'name': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'age': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'city': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'instagram_username': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Мой ответ'}, ),
            'tg_channel_url': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'tg_username': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'policy_agreement': forms.CheckboxInput(attrs={'style': 'display:none'}),
            'marketing_type': forms.RadioSelect,
            'average_income': forms.RadioSelect,
            'medblog': forms.RadioSelect,
            'how_warmed_up': forms.RadioSelect,
            'rate_of_employment': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

        self.fields['email'].error_messages.update({
            'invalid': 'Введите правильный адрес электронной почты.'
        })

        self.fields['marketing_type'].error_messages.update({
            'required': 'Обязательное поле'
        })

        self.fields['average_income'].error_messages.update({
            'required': 'Обязательное поле'
        })

        self.fields['medblog'].error_messages.update({
            'required': 'Обязательное поле'
        })

        self.fields['how_warmed_up'].error_messages.update({
            'required': 'Обязательное поле'
        })

        self.fields['rate_of_employment'].error_messages.update({
            'required': 'Обязательное поле'
        })

        self.fields['have_bought_products'].error_messages.update({
            'required': 'Обязательное поле'
        })

        self.fields['marketing_type'].choices = list(ExpressMedbloger.MARKETING_TYPE_CHOICES)
        self.fields['average_income'].choices = list(ExpressMedbloger.AVERAGE_INCOME_CHOICES)
        self.fields['medblog'].choices = list(ExpressMedbloger.MEDBLOG_CHOICES)

        self.fields['how_warmed_up'].choices = list(ZERO_TO_TEN_CHOICES)
        self.fields['rate_of_employment'].choices = list(ZERO_TO_TEN_CHOICES)
