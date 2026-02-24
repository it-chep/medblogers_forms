from django import forms
from business_forms.models import MedblogersPreEntry, NationalBlogersAssociation, ExpressMedbloger, ZERO_TO_TEN_CHOICES, \
    NeuroMedbloger, SMMSpecialists, Speecadoc, MedSMM, ONE_TO_TEN_CHOICES


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
            'speciality': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'medblog_reason': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'medblog_complexity': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'medblog_helped': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'how_long_following': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'top_questions': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'name': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'age': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'city': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'instagram_username': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'phone': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'email': forms.EmailInput(attrs={'placeholder': 'Мой ответ'}, ),
            'tg_channel_url': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'tg_username': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, 'required': True}
            ),
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

        self.fields['speciality'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['medblog_reason'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['medblog_complexity'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['medblog_helped'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['how_long_following'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['top_questions'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['name'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['age'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['city'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['instagram_username'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['phone'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['tg_channel_url'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['tg_username'].error_messages.update({
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
        self.fields['rate_of_employment'].choices = list(ZERO_TO_TEN_CHOICES)  # ExpressMedblogerForm


class NeuroMedblogerForm(forms.ModelForm):
    """Нейросети для медблога"""

    class Meta:
        model = NeuroMedbloger
        fields = (
            "name",
            "city",
            "speciality",
            "phone",
            "email",
            "tg_username",
            "level_of_use_neuro",
            "your_questions",
            "policy_agreement",
        )
        widgets = {
            'speciality': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'name': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'city': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Мой ответ'}, ),
            'tg_username': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'policy_agreement': forms.CheckboxInput(attrs={'style': 'display:none'}),
            'level_of_use_neuro': forms.RadioSelect,
            'your_questions': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

        self.fields['email'].error_messages.update({
            'invalid': 'Введите правильный адрес электронной почты.'
        })

        self.fields['level_of_use_neuro'].error_messages.update({
            'required': 'Обязательное поле'
        })

        self.fields['level_of_use_neuro'].choices = list(ZERO_TO_TEN_CHOICES)


class SMMForm(forms.ModelForm):
    """Работали с помощником по блогу? Поделитесь опытом"""

    class Meta:
        model = SMMSpecialists
        fields = (
            "specialization",
            "social_networks",
            "your_experience",
            "last_collaboration_period",
            "satisfied_of_results",
            "positive_specialist_contact",
            "negative_specialist_contact",
            "user_contact",
        )
        widgets = {
            'specialization': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'last_collaboration_period': forms.RadioSelect,
            'satisfied_of_results': forms.RadioSelect,
            'positive_specialist_contact': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'negative_specialist_contact': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'user_contact': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'social_networks': forms.CheckboxSelectMultiple,
            'your_experience': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages.update({
                'required': 'Обязательное поле'
            })
            field.required = True

        self.fields['last_collaboration_period'].choices = list(SMMSpecialists.LAST_COLLABORATION_PERIOD_CHOICES)
        self.fields['satisfied_of_results'].choices = list(SMMSpecialists.SATISFIED_OF_RESULT_CHOICES)

        self.fields['social_networks'].choices = list(SMMSpecialists.SOCIAL_NETWORKS_CHOICES)
        self.fields['social_networks'].required = False
        self.fields['your_experience'].choices = list(SMMSpecialists.YOUR_EXPERIENCE_CHOICES)
        self.fields['your_experience'].required = False


class SpeecadocForm(forms.ModelForm):
    """Настав кати"""

    class Meta:
        model = Speecadoc
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
            'speciality': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'medblog_reason': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'medblog_complexity': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'medblog_helped': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'how_long_following': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'top_questions': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'name': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'age': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'city': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'instagram_username': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'phone': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'email': forms.EmailInput(attrs={'placeholder': 'Мой ответ'}, ),
            'tg_channel_url': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'tg_username': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, 'required': True}
            ),
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

        self.fields['speciality'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['medblog_reason'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['medblog_complexity'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['medblog_helped'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['how_long_following'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['top_questions'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['name'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['age'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['city'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['instagram_username'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['phone'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['tg_channel_url'].error_messages.update({
            'required': 'Обязательное поле'
        })
        self.fields['tg_username'].error_messages.update({
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

        self.fields['marketing_type'].choices = list(Speecadoc.MARKETING_TYPE_CHOICES)
        self.fields['average_income'].choices = list(Speecadoc.AVERAGE_INCOME_CHOICES)
        self.fields['medblog'].choices = list(Speecadoc.MEDBLOG_CHOICES)

        self.fields['how_warmed_up'].choices = list(ZERO_TO_TEN_CHOICES)
        self.fields['rate_of_employment'].choices = list(ZERO_TO_TEN_CHOICES)


class MedSMMForm(forms.ModelForm):
    """Опрос для будущих медицинских SMM-специалистов"""

    class Meta:
        model = MedSMM
        fields = (
            "marketing_type",
            "age_range",
            "occupation",
            "average_income",
            "reason_for_career_change",
            "disappointment_level",
            "tried_blogging",
            "smm_education",
            "skills",
            "smm_work_vision",
            "desired_income",
            "top_fears",
            "investment_readiness",
            "five_year_plan",
            "name",
            "city",
            "instagram_username",
            "tg_username",
            "email",
            "phone",
            "policy_agreement",
        )
        widgets = {
            'reason_for_career_change': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'smm_work_vision': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'top_fears': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'five_year_plan': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'name': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'city': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'instagram_username': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'tg_username': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'phone': forms.Textarea(
                attrs={'placeholder': 'Мой ответ', 'class': 'auto-resize-textarea', 'rows': 1, }
            ),
            'email': forms.EmailInput(attrs={'placeholder': 'Мой ответ'}),
            'policy_agreement': forms.CheckboxInput(attrs={'style': 'display:none'}),
            'marketing_type': forms.RadioSelect,
            'age_range': forms.RadioSelect,
            'average_income': forms.RadioSelect,
            'tried_blogging': forms.RadioSelect,
            'smm_education': forms.RadioSelect,
            'desired_income': forms.RadioSelect,
            'investment_readiness': forms.RadioSelect,
            'disappointment_level': forms.RadioSelect,
            'skills': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages.update({
                'required': 'Обязательное поле'
            })
            field.required = True

        self.fields['email'].error_messages.update({
            'invalid': 'Введите правильный адрес электронной почты.'
        })

        self.fields['skills'].required = False

        # Поля после "мощного бонуса" — необязательные
        bonus_fields = ['name', 'city', 'instagram_username', 'tg_username', 'email', 'phone']
        for field_name in bonus_fields:
            self.fields[field_name].required = False

        # Occupation приходит через чекбоксы, а не через Django-виджет
        self.fields['occupation'].required = False
        self.fields['occupation'].choices = list(MedSMM.OCCUPATION_CHOICES)

        self.fields['marketing_type'].choices = list(MedSMM.MARKETING_TYPE_CHOICES)
        self.fields['age_range'].choices = list(MedSMM.AGE_RANGE_CHOICES)
        self.fields['average_income'].choices = list(MedSMM.AVERAGE_INCOME_CHOICES)
        self.fields['tried_blogging'].choices = list(MedSMM.TRIED_BLOGGING_CHOICES)
        self.fields['smm_education'].choices = list(MedSMM.SMM_EDUCATION_CHOICES)
        self.fields['desired_income'].choices = list(MedSMM.DESIRED_INCOME_CHOICES)
        self.fields['investment_readiness'].choices = list(MedSMM.INVESTMENT_READINESS_CHOICES)
        self.fields['disappointment_level'].choices = list(ONE_TO_TEN_CHOICES)
        self.fields['skills'].choices = list(MedSMM.SKILLS_CHOICES)
