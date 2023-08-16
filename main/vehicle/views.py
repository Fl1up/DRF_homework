from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from main.vehicle.models import Course, Lessons, Pay, Subscription
from main.vehicle.paginators import VehiclePaginator
from main.vehicle.serializers import CourseSerializer, LessonSerializer, CourseCreateSerializer, LessonCreateSerializer,PaySerializer, LessonPaymentSerializer, SubscriptionSerializer


class CourseViewSet(ModelViewSet):  # все для ViewSet
    """Course View"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes = [AllowAny]  # для не автор пользователей этого видно не будет(ошибка по выводу инфы)
    pagination_class = VehiclePaginator  # Пагинация

    # def post(self, *args, **kwargs):  # во ViewSet пост отвечает за создание
    #     self.serializer_class = CourseCreateSerializer  # Это ViewSet тоже-самое что и с LessonCreateAPIView
    #     super()


class LessonCreateAPIView(generics.CreateAPIView):  # все для Generic
    """Create Lesson"""
    serializer_class = LessonCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):  # сохранения нового владельца при создании нового урока
        mew_lesson = serializer.save()
        mew_lesson.owner = self.request.user  # owner - владелец  (нужно добавить в models)
        mew_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Lesson List"""
    serializer_class = LessonSerializer
    queryset = Lessons.objects.all()
    permission_classes = [AllowAny]
    pagination_class = VehiclePaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Lesson Retrive"""
    serializer_class = LessonSerializer
    queryset = Lessons.objects.all()
    permission_classes = [AllowAny]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Lesson Updaate"""
    serializer_class = LessonSerializer
    queryset = Lessons.objects.all()
    permission_classes = [AllowAny]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Lesson Delete"""
    queryset = Lessons.objects.all()
    permission_classes = [AllowAny]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Payment Create"""
    serializer_class = PaySerializer
    permission_classes = [AllowAny]


class PaymentListAPIView(generics.ListAPIView):  # Фильтр
    """Payment List"""
    serializer_class = PaySerializer
    queryset = Pay.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson")
    ordering_fields = ("payment_date",)
    pagination_class = VehiclePaginator


class LessonPaymentAPIView(generics.ListAPIView):
    """Lesson Pyment"""
    serializer_class = LessonPaymentSerializer
    queryset = Pay.objects.filter(lesson__isnull=False)  # уроки должны быть заполненны
    pagination_class = VehiclePaginator
    # permission_classes = [AllowAny]

class PayCreateAPIView(generics.CreateAPIView):
    """Создание оплаты"""

    serializer_class = PaySerializer


class PayListAPIView(generics.ListAPIView):
    """Просмотр списка оплат"""

    serializer_class = PaySerializer
    queryset = Pay.objects.all()
    pagination_class = VehiclePaginator
    filter_backends = [SearchFilter, OrderingFilter]
    # Фильтры
    search_fields = ["payment_type", "course_name", "lesson_name"]
    # Сортировка прямая / обратная
    ordering_fields = ["pay_date"]
    ordering = ["-pay_date"]


class PayRetrieveAPIView(generics.RetrieveAPIView):
    """Отображение элемента  - оплаты"""

    serializer_class = PaySerializer
    queryset = Pay.objects.all()


class PayUpdateAPIView(generics.UpdateAPIView):
    """Изменение элемента - оплаты"""

    serializer_class = PaySerializer
    queryset = Pay.objects.all()


class PayDestroyAPIView(generics.DestroyAPIView):
    """Удаление элемента  - оплаты"""

    queryset = Pay.objects.all()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Создание подписки"""

    serializer_class = SubscriptionSerializer


class SubscriptionListAPIView(generics.ListAPIView):
    """Просмотр списка подписок"""

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    pagination_class = SubscriptionSerializer


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    """Отображение элемента подписки """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """Изменение элемента подписки"""

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Удаление элемента подписки"""

    queryset = Subscription.objects.all()

