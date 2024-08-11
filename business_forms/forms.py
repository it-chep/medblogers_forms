from django import forms
from business_forms.models import MedblogersPreEntry, NationalBlogersAssociation


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
