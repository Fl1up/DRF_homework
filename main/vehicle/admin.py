from django.contrib import admin

from main.vehicle.models import Course, Lessons , Pay


# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_name", "course_description")  # отображение на дисплее
    list_filter = ("course_name", "course_description")  # фильтр
    search_fields = ("course_name", "course_description")  # поля поиска

@admin.register(Lessons)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("lesson_name", "lesson_description")  # отображение на дисплее
    list_filter = ("lesson_name", "lesson_description")  # фильтр
    search_fields = ("lesson_name", "lesson_description")  # поля поиска

@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ("pay_date", "pay_sum", "payment_type")  # отображение на дисплее
    list_filter = ("pay_date", "pay_sum", "payment_type")  # фильтр
    search_fields = ("pay_date", "pay_sum", "payment_type")  # поля поиска