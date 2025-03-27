from django import forms
from django.core.exceptions import ValidationError
import re


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш Email'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше сообщение',
            'rows': 5
        })
    )

    g_recaptcha_response = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', name):
            raise ValidationError("Имя содержит недопустимые символы")
        return name

    def clean_message(self):
        message = self.cleaned_data['message'].strip()
        if len(message) < 5:
            raise ValidationError("Сообщение слишком короткое")
        return message

    def clean_g_recaptcha_response(self):
        recaptcha_response = self.cleaned_data.get('g_recaptcha_response')
        if not recaptcha_response:
            raise ValidationError("Пожалуйста, пройдите проверку reCAPTCHA")
        return recaptcha_response
