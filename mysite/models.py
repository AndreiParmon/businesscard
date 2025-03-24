from PIL import Image
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, blank=False, verbose_name="Имя")
    image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Фотография профиля',
                              default='profiles/default.jpg')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    phone_number = models.CharField(max_length=13, blank=True, null=True, verbose_name='Номер телефона')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        max_width, max_height = 250, 250

        if img.height > max_height or img.width > max_width:
            output_size = (max_width, max_height)
            img.thumbnail(output_size)
            img.save(self.image.path)
