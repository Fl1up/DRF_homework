import stripe
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from main.vehicle.models import Course, Lessons, Pay, Subscription
from main.vehicle.validators import TitleValidator


class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"



class LessonSerializer(serializers.ModelSerializer):
    """Сериалайзер"""

    validators = [
        TitleValidator(field="lesson_video_url")
    ]  # Проверка валидности видео

    class Meta:
        model = Lessons
        fields = "__all__"



class CourseSerializer(serializers.ModelSerializer):
    # добавление поля количество уроков  через описание нового типа, и сслыкой на запрос к лесссон, суммирование
    lessons_count = serializers.IntegerField(
        source="lesson_set.all.count", read_only=True
    )
    # Добавление в сериализатор уроков для курса, смотри функцию get_lessons

    lessons = serializers.SerializerMethodField(read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)
    payments = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons(self, instance):
        """Добавление уроков для курса"""
        lesson_list = []
        if instance.lesson_set.all():
            for i in instance.lesson_set.all().values_list():
                lesson_list.append(i[1])
            return lesson_list
        return None

    def get_subscription(self, instance):
        """Добавление подписки для курса"""
        request = self.context.get("request")
        user = request.user
        sub_all = instance.subscription.all()
        for sub in sub_all:
            if sub.subscriber == user:
                return True
        return False

    def get_payments(self, course):
        """Добавление оплаты для курса"""
        #создание продукта с именем, которое берется из имени курса ( course.course_name)
        payment = stripe.Product.create(name=course.course_name, )
        #Создание цены на продукт:
        price = stripe.Price.create(
            # сумма
            unit_amount=int(course.price*100),
            # валюта
            currency="usd",
            # привязка к продукту
            product=payment['id'],
        )
        #Создание платежной сессии
        session = stripe.checkout.Session.create(
            # адрес после успешного платежа
            success_url="https://example.com/success",
            # при неудаче
            cancel_url="https://example.com/cancel",
            # Тип платежного метода
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price['id'],
                    # количество
                    "quantity": 1,
                },
            ],
            # Режим платежа,(что такое не понял)
            mode="payment",
        )
        #Возврат URL-адреса для оплаты
        return session['url']

    def get_lessons_view(self, obj):
        lessons = Lessons.objects.filter(course=obj)
        return LessonSerializer(lessons, many=True).data  # Указываем, что на вход подаётся набор записей

    def get_lessons_information_view(self, obj):
        return obj.lesson

    def get_lessons_count(self, obj):  # вывод числа
        return obj.lessons.count()

    def get_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            subscription = Pay.objects.filter(
                user=user,
                course=obj
            ).first()
            if subscription:
                return subscription.subscribed
        return False


class LessonPaymentSerializer(serializers.ModelSerializer):  # конкретно под уроки
    serializer_class = LessonSerializer
    queryset = Pay.objects.all()

    class Meta:
        model = Pay
        fields = ("lesson",)


class LessonCreateSerializer(serializers.ModelSerializer):
    payment = PaySerializer(many=True, read_only=True)

    class Meta:
        model = Lessons
        fields = "__all__"

    def create(self, validated_data):
        payment = validated_data.get("payment", [])  # выдергивание ключа "payment" с проверкой наличия
        lesson_item = Lessons.objects.create(**validated_data)

        if payment:
            for m in payment:
                Pay.objects.create(**m, lesson=lesson_item)

        return lesson_item



class CourseCreateSerializer(serializers.ModelSerializer):
    payment = PaySerializer(many=True, read_only=True)  # Указываем, что на вход подаётся набор записей

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):

        payment = validated_data.pip("payment") # выдергивание ключа "payment"

        course_item = Lessons.objects.create(**validated_data)

        for m in payment:
            Pay.objects.create(**m, course=course_item)

        return course_item

class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериалайзер"""

    class Meta:
        model = Subscription
        fields = "__all__"
#

