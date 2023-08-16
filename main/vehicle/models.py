from django.conf import settings
from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

from main.users.models import User

# Create your models here.
NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    course_name = models.CharField(max_length=100, verbose_name="название курса")
    course_description = models.TextField(verbose_name="описание курса", **NULLABLE)
    course_preview = models.ImageField(
        upload_to="course/", verbose_name="изображение", **NULLABLE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE
    )
    price = models.FloatField(default=1000.00, verbose_name='Цена USD')


    def __str__(self):
        return f"{self.course_name} {self.course_description}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lessons(models.Model):
    lesson_name = models.CharField(max_length=100, verbose_name="название урока")
    lesson_description = models.TextField(verbose_name="описание урока", **NULLABLE)
    lesson_preview = models.ImageField(
        upload_to="course/", verbose_name="изображение", **NULLABLE
    )
    lesson_video_url = models.CharField(
        max_length=255, verbose_name="ссылка на видео", **NULLABLE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE
    )

    def __str__(self):
        return f"{self.lesson_name} {self.lesson_description}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"



class Pay(models.Model):
    CHOICES = (
        ("Card", "карта"),
        ("CASH", "наличка"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    pay_date = models.DateField(verbose_name="дата платежа", auto_now=True)
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, **NULLABLE)
    pay_sum = models.IntegerField(verbose_name="сумма платежа")
    payment_type = models.CharField(choices=CHOICES, verbose_name="тип оплаты")

    def __str__(self):
        return f"{self.user} {self.course_name}"

    class Meta:
        verbose_name = "оплата"
        verbose_name_plural = "оплаты"


class Subscription(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        **NULLABLE,
        related_name="subscription",
        verbose_name="Подписка на курс",
    )
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        **NULLABLE,
    )

    def __str__(self):
        return f"{self.course}:{self.subscriber}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
