from django.db import models


class TestDBUser(models.Model):
    user = models.CharField('Пользователь', max_length=32)
    text = models.TextField('Текст')

    def __str__(self):
        return self.user