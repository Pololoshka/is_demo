from django.db import models

class NumberChoicesAddToChat(models.IntegerChoices):
    zero = 0, 'Не уведомлять'
    one = 1, 'Уведомлять'