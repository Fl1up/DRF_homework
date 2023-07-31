from django.urls import path

from main.vehicle.apps import VehicleConfig
from rest_framework.routers import DefaultRouter

from main.vehicle.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

# все для ViewSet
app_name = VehicleConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

# все для Generic
urlpatterns = [
    path("Lesson/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("Lesson/", LessonListAPIView.as_view(), name="lesson-list"),
    path("Lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-get"),
    path("Lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("Lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"),

] + router.urls