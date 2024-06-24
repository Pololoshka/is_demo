from django.db import models


class NumberChoicesType(models.IntegerChoices):
    one = 1, 'Исходящий'
    two = 2, 'Входящий'
    three = 3, 'Входящий с перенаправлением'
    four = 4, 'Обратный'
