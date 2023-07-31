from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    preview = models.ImageField(verbose_name="Превью", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название", default="")
    preview = models.ImageField(verbose_name="Превью", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    url_video = models.CharField(max_length=50, verbose_name="Ссылка на видео", default="")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
