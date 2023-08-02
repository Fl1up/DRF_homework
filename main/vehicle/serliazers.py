from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from main.vehicle.models import Course, Payment, Lesson


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("course", "description", "url_video")


class CourseSerializer(serializers.ModelSerializer):
    lessons_information = PaymentSerializer(source="payment", many=True)
    lessons = LessonSerializer(source="payment", many=True)
    lessons_count = SerializerMethodField(source="payment")  # вывод числа

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_view(self, obj):
        lessons = Lesson.objects.filter(course=obj)
        return LessonSerializer(lessons, many=True).data

    def get_lessons_information_view(self, obj):
        return obj.lesson

    def get_lessons_count(self, obj):   # вывод числа
        return obj.lessons.count()


class LessonPaymentSerializer(serializers.ModelSerializer):  # конкретно под уроки
    serializer_class = LessonSerializer
    queryset = Payment.objects.all()

    class Meta:
        model = Payment
        fields = ("lesson",)


class LessonCreateSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = "__all__"

    def create(self, validated_data):
        payment = validated_data.pop("payment")  # выдергивание ключа "payment"

        lesson_item = Lesson.objects.create(**validated_data)

        for m in payment:
            Payment.objects.create(**m, lesson=lesson_item)

        return lesson_item


class CourseCreateSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        payment = validated_data.pip("payment")  # выдергивание ключа "payment"

        course_item = Lesson.objects.create(**validated_data)

        for m in payment:
            Payment.objects.create(**m, course=course_item)

        return course_item
