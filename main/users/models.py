from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="электронная почта")
    phone = models.CharField(max_length=50, verbose_name="телефон", **NULLABLE)
    avatar = models.ImageField(upload_to="users/", verbose_name="аватар", **NULLABLE)
    country = models.CharField(max_length=20, verbose_name="страна", **NULLABLE)
    first_name = models.CharField(max_length=25, verbose_name="имя")
    last_name = models.CharField(max_length=25, verbose_name="фамилия", **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name="активный")

    # переопределение поля user  как основного для идентификации на емаил
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"