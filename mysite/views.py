import time
from django.conf import settings
import requests
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.views import View
from .forms import ContactForm
from .models import Profile
from django.shortcuts import render


def home(request):
    name = Profile.objects.get()
    context = {
        'name': name
    }
    return render(request, 'mysite/home.html', context)


def my_view(request):
    current_page = request.path
    return render(request, 'template.html', {'current_page': current_page})


class ContactView(View):
    template_name = 'mysite/contact.html'
    success_template = 'mysite/contact_success.html'
    RATE_LIMIT = 3  # Максимальное количество запросов
    RATE_LIMIT_TIME = 60  # В секундах (1 минута)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def is_rate_limited(self, request):
        ip = self.get_client_ip(request)
        cache_key = f'contact_rate_limit_{ip}'

        current_time = time.time()
        request_times = cache.get(cache_key, [])

        request_times = [t for t in request_times if current_time - t < self.RATE_LIMIT_TIME]

        if len(request_times) >= self.RATE_LIMIT:
            return True

        request_times.append(current_time)
        cache.set(cache_key, request_times, self.RATE_LIMIT_TIME)
        return False

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, {
            'form': form,
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
        })

    def post(self, request):
        # Проверка ограничения запросов
        if self.is_rate_limited(request):
            return render(request, self.template_name, {
                'form': ContactForm(request.POST),
                'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
                'error': 'Слишком много запросов. Пожалуйста, попробуйте позже.'
            }, status=429)

        form = ContactForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
            })

        # Проверка reCAPTCHA
        try:
            secret_key = settings.RECAPTCHA_SECRET_KEY
            payload = {
                "secret": secret_key,
                "response": form.cleaned_data['g_recaptcha_response'],
                "remoteip": self.get_client_ip(request)
            }

            response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data=payload,
                timeout=5
            )
            result = response.json()

            if not result.get("success"):
                form.add_error(None, "Ошибка проверки reCAPTCHA. Пожалуйста, попробуйте снова.")
                return render(request, self.template_name, {
                    'form': form,
                    'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
                })

        except requests.RequestException as e:
            form.add_error(None, "Ошибка соединения с сервисом проверки. Пожалуйста, попробуйте позже.")
            return render(request, self.template_name, {
                'form': form,
                'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
            })

        # Отправка email
        try:
            user_name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            email = EmailMessage(
                subject=f"Сообщение от {user_name}",
                body=f"Вы получили сообщение от {user_name} ({user_email}):\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL],
                reply_to=[user_email]
            )
            email.send()

            return render(request, self.success_template)

        except Exception as e:
            form.add_error(None, "Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте позже.")
            return render(request, self.template_name, {
                'form': form,
                'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY
            })


def about(request):
    return render(request, 'mysite/about.html')
