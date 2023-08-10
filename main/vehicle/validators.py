import re

from rest_framework.serializers import ValidationError


class TitleValidator:

    def __init__(self, field):
        self.field = field  # Сохранение его

    def __call__(self, value):  # проверка полученного результата
        for values in value:
            if not re.search("(?i)\b(?!youtube\.com)\w+\.\w{2,3}\b", values):
                return ValidationError("Title is not ok")
        return True
