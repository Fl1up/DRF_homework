from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

from main.users.models import User

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
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, default="")
    title = models.CharField(max_length=50, verbose_name="Название", default="")
    preview = models.ImageField(verbose_name="Превью", **NULLABLE)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    url_video = models.CharField(max_length=50, verbose_name="Ссылка на видео", default="")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Payment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name="payment")  # обращение через ключевое слово, а не через payment_set
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name="payment")  # обращение через ключевое слово, а не через payment_set

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    payment_date = models.DateField(verbose_name="Дата оплаты", auto_now_add=True)
    course_or_lesson = models.CharField(max_length=100, choices=[
        ("course", "Курс"),
        ("lesson", "Урок")
    ])
    payment_amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Сумма отплаты")
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    ], verbose_name="Метод отплаты")

    def __str__(self):
        return f"{self.id} - {self.user.username} оплатил: {self.course if self.course else self.lesson}"

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"