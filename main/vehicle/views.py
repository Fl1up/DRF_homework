from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from main.vehicle.models import Course, Lesson, Payment
from main.vehicle.serliazers import CourseSerializer, LessonSerializer, PaymentSerializer, LessonPaymentSerializer, \
    LessonCreateSerializer, CourseCreateSerializer


class CourseViewSet(ModelViewSet):  # все для ViewSet
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    # def post(self, *args, **kwargs):  # во ViewSet пост отвечает за создание
    #     self.serializer_class = CourseCreateSerializer  # Это ViewSet тоже-самое что и с LessonCreateAPIView
    #     super()


class LessonCreateAPIView(generics.CreateAPIView):  # все для Generic
    serializer_class = LessonCreateSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson")
    ordering_fields = ("payment_date",)


class LessonPaymentAPIView(generics.ListAPIView):
    serializer_class = LessonPaymentSerializer
    queryset = Payment.objects.filter(lesson__isnull=False)  # уроки должны быть заполненны



