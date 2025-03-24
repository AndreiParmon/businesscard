from django.conf import settings
import requests
from django.core.mail import EmailMessage

from .models import Profile
from django.shortcuts import render


def home(request):
    # name = Profile.objects.get()
    # context = {
    #     'name': name
    # }
    # return render(request, 'mysite/home.html', context)


    return render(request, 'mysite/home.html')


def contact(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        message = request.POST.get('message')
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Проверка reCAPTCHA
        secret_key = settings.RECAPTCHA_SECRET_KEY
        payload = {"secret": secret_key, "response": recaptcha_response}
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
        result = response.json()

        if not result.get("success"):
            return render(request, 'mysite/contact.html', {
                "error": "Ошибка reCAPTCHA. Попробуйте снова.",
                "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY
            })

        # Отправка email
        subject = f"Сообщение от {user_name}"
        email_message = f"Вы получили сообщение от {user_name} ({user_email}):\n\n{message}"

        email = EmailMessage(
            subject=subject,
            body=email_message,
            from_email='andrei.parmon@yandex.ru',
            to=['parmonandrei@gmail.com'],
            headers={'Reply-To': user_email}
        )
        email.send()

        return render(request, 'mysite/contact_success.html')

    return render(request, 'mysite/contact.html', {"recaptcha_site_key": settings.RECAPTCHA_SITE_KEY})


# def contact(request):
#    if request.method == 'POST':
#        user_name = request.POST.get('name')
#        user_email = request.POST.get('email')
#        message = request.POST.get('message')
#
#        subject = f"Сообщение от {user_name}"
#        email_message = f"Вы получили сообщение от {user_name} ({user_email}):\n\n{message}"
#
#   email = EmailMessage(
#       subject=subject,
#       body=email_message,
#       from_email='andrei.parmon@yandex.ru',
#       to=['parmonandrei@gmail.com'],
#       headers={'Reply-To': user_email}
#   )
#   email.send()
#   return render(request, 'mysite/contact_success.html')
# return render(request, 'mysite/contact.html')


def about(request):
    return render(request, 'mysite/about.html')
