import re

from rest_framework.serializers import ValidationError


class TitleValidator:
    """Класс валидации данных в заданном формате. для Уроков"""

    def __init__(self, field):
        """Магический метод, берем пеерменную поля для ввода данных и проверки"""
        self.field = field

    def __call__(self, value):
        """Магический метод, осуществляем проверку валидации данных"""
        field_new = dict(value).get(self.field)
        if field_new:
            if not bool(re.search(r"youtube.com", field_new)):
                raise ValidationError("Возможно размещение видео только на YouTube")