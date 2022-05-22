from django.db import models
from django.contrib.auth.models import User


class TestDBUser(models.Model):
    user = models.CharField('Пользователь', max_length=32)
    text = models.TextField('Текст')

    def __str__(self):
        return self.user


class Core(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    credits = models.IntegerField(default=1)
    click_power = models.IntegerField(default=1)

    def click(self, commit=True):
        self.coins += self.click_power
        if commit:
            self.save()
        return self.coins