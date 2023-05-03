from django.contrib.auth import get_user_model
from django.db import models

from base.infra.models import BaseModel


User = get_user_model()


class Unit(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    is_active = models.BooleanField()

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return self.title


class Attribute(BaseModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    is_active = models.BooleanField()

    class Meta:
        verbose_name = 'Аттрибут'
        verbose_name_plural = 'Аттрибуты'

    def __str__(self):
        return self.title
