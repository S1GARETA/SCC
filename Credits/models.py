from copy import copy
from django.db import models
from django.contrib.auth.models import User
from .constanrs import *


class Core(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    coins_per_second = models.IntegerField(default=0)
    credits = models.IntegerField(default=1)
    click_power = models.IntegerField(default=1)

    def update_coins(self, coins, commit=True):
        self.coins = coins
        if commit:
            self.save()

        return self.coins


    def click(self, commit=True):
        self.coins += self.click_power
        if commit:
            self.save()

        return self.coins


class Boost(models.Model):
    core = models.ForeignKey(Core, null=False, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)
    power = models.IntegerField(default=1)
    name = models.CharField(default='boostname', max_length=32)
    type = models.PositiveSmallIntegerField(
        default=0,
        choices=BOOST_TYPE_CHOICES,
    )

    def levelup(self, coins):
        if coins < self.price:
            return False

        self.core.coins -= self.price
        self.core.click_power += self.power * BOOST_TYPE_VALUES[self.type]['click_power_scale']
        self.core.coins_per_second += self.power * BOOST_TYPE_VALUES[self.type]['auto_click_power_scale']
        self.core.save()

        old_boost_values = copy(self)

        self.level += 1
        self.power += 1
        self.price += self.price * BOOST_TYPE_VALUES[self.type]['price_scale']

        self.save()

        return old_boost_values, self