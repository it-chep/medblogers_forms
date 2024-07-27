from django import forms
from business_forms.models import MedblogersPreEntry


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
            'email': forms.EmailInput(attrs={'placeholder': 'Мой ответ'},),
            'phone': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'instagram_username': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'tg_username': forms.TextInput(attrs={'placeholder': 'Мой ответ'}),
            'policy_agreement': forms.CheckboxInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

        self.fields['email'].error_messages.update({
            'invalid': 'Введите правильный адрес электронной почты.'
        })
