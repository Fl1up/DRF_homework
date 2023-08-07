from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from main.vehicle.models import Course, Lesson, Payment
from main.vehicle.permissions import IsOwnerOrStaff
from main.vehicle.serliazers import CourseSerializer, LessonSerializer, PaymentSerializer, LessonPaymentSerializer, \
    LessonCreateSerializer, CourseCreateSerializer


class CourseViewSet(ModelViewSet):  # все для ViewSet
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]  # для не автор пользователей этого видно не будет(ошибка по выводу инфы)

    # def post(self, *args, **kwargs):  # во ViewSet пост отвечает за создание
    #     self.serializer_class = CourseCreateSerializer  # Это ViewSet тоже-самое что и с LessonCreateAPIView
    #     super()


class LessonCreateAPIView(generics.CreateAPIView):  # все для Generic
    serializer_class = LessonCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):  # сохранения нового владельца при создании нового урока
        mew_lesson = serializer.save()
        mew_lesson.owner = self.request.user  # owner - владелец  (нужно добавить в models)
        mew_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentListAPIView(generics.ListAPIView):  # Фильтр
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson")
    ordering_fields = ("payment_date",)


class LessonPaymentAPIView(generics.ListAPIView):
    serializer_class = LessonPaymentSerializer
    queryset = Payment.objects.filter(lesson__isnull=False)  # уроки должны быть заполненны



