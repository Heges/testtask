import jwt

from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, User
from django.contrib.auth.models import PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver
from django.db.models.signals import post_save


class Masters(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'


class Service(models.Model):
    worked_hours = (
        ('1', '10:00'),
        ('2', '11:00'),
        ('3', '12:00'),
        ('4', '13:00'),
        ('5', '14:00'),
        ('6', '15:00'),
        ('7', '16:00'),
        ('8', '17:00'),
        ('9', '18:00'),
        ('10', '19:00'),
        ('11', '20:00'),
    )

    name_master = models.ForeignKey(Masters, verbose_name='Мастер', on_delete=models.CASCADE)
    client_to_job = models.ForeignKey(User, verbose_name='Клиент', on_delete=models.CASCADE)
    work_on = models.CharField(verbose_name='Рабочие часы', choices=worked_hours, max_length=30)

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    info_car = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_tokens_for_user(cls, user):
        cls.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get_user_id(self):
        return self.user_id
