import stripe
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from main.vehicle.models import Course, Payment, Lesson, CourseSubscription
from main.vehicle.services import payment
from main.vehicle.validators import TitleValidator


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("course", "description", "url_video")


class CourseSerializer(serializers.ModelSerializer):
    lessons_information = PaymentSerializer(source="payment",
                                            many=True, read_only=True)  # Указываем, что на вход подаётся набор записей
    lessons = LessonSerializer(source="payment", many=True, read_only=True)  # Указываем, что на вход подаётся набор записей
    lessons_count = SerializerMethodField(source="payment")  # вывод числа
    subscribed = serializers.SerializerMethodField()


    class Meta:
        model = Course
        fields = '__all__'
        validators = \
            [TitleValidator(field="title"),
             serializers.UniqueTogetherValidator(fields=["title"], queryset=Course.objects.all())  # Уникальность
             ]

        def get_subscribed(self, instance):
            return payment(instance.amount)

    def get_lessons_view(self, obj):
        lessons = Lesson.objects.filter(course=obj)
        return LessonSerializer(lessons, many=True).data  # Указываем, что на вход подаётся набор записей

    def get_lessons_information_view(self, obj):
        return obj.lesson

    def get_lessons_count(self, obj):  # вывод числа
        return obj.lessons.count()

    def get_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            subscription = CourseSubscription.objects.filter(
                user=user,
                course=obj
            ).first()
            if subscription:
                return subscription.subscribed
        return False


class LessonPaymentSerializer(serializers.ModelSerializer):  # конкретно под уроки
    serializer_class = LessonSerializer
    queryset = Payment.objects.all()

    class Meta:
        model = Payment
        fields = ("lesson",)


class LessonCreateSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = "__all__"

    def create(self, validated_data):
        payment = validated_data.get("payment", [])  # выдергивание ключа "payment" с проверкой наличия
        lesson_item = Lesson.objects.create(**validated_data)

        if payment:
            for m in payment:
                Payment.objects.create(**m, lesson=lesson_item)

        return lesson_item



class CourseCreateSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True)  # Указываем, что на вход подаётся набор записей

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):

        payment = validated_data.pip("payment") # выдергивание ключа "payment"

        course_item = Lesson.objects.create(**validated_data)

        for m in payment:
            Payment.objects.create(**m, course=course_item)

        return course_item

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = "__all__"


def payment(request):
    if request.method == 'POST':
        stripe.api_key = 'sk_test_51NexkmDyPJ4N4cRkA0ddCgzqu35kFSAYhrDChFbJKTWYYdmjFSXhWxNSExsSCAehSPhywRgXDD3EmB8Ib7D5Fc4m0074WtOdLC:'
        token = request.POST.get('stripeToken')
        amount = request.POST.get('amount')

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
                description='Payment for course'
            )
            # Здесь можно добавить логику обработки успешного платежа
            return render(request, 'success.html')
        except stripe.error.CardError as e:
            # Обработка ошибки оплаты
            pass
    return render(request, 'payment.html')