# Create your models here.
from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания"""
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    edited = models.DateTimeField(
        'Дата изменения',
        auto_now=True
    )
    
    class Meta():
        abstract = True