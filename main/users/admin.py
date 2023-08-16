
from django.contrib import admin
from main.users.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "country")  # отображение на дисплее
    list_filter = ("email", "phone", "country")  # фильтр
    search_fields = ("email", "phone", "country")  # поля поиска
