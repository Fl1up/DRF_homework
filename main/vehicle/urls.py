from django.urls import path
from rest_framework.routers import DefaultRouter

from main.vehicle.apps import VehicleConfig
from main.vehicle.views import CourseViewSet, LessonCreateAPIView, LessonRetrieveAPIView, LessonListAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PayCreateAPIView, PayListAPIView, PayUpdateAPIView, PayRetrieveAPIView, \
    PayDestroyAPIView, SubscriptionCreateAPIView, SubscriptionListAPIView, SubscriptionRetrieveAPIView, \
    SubscriptionUpdateAPIView, SubscriptionDestroyAPIView

# все для ViewSet
app_name = VehicleConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="course")

# все для Generic
urlpatterns = [
    #
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/list/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/deteil/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_deteil"),
    path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),

    # Payment
    path("payment/create/", PayCreateAPIView.as_view(), name="pay_create"),
    path("payment/list/", PayListAPIView.as_view(), name="pay_list"),
    path("payment/deteil/<int:pk>/", PayRetrieveAPIView.as_view(), name="pay_deteil"),
    path("payment/update/<int:pk>/", PayUpdateAPIView.as_view(), name="pay_update"),
    path("payment/delete/<int:pk>/", PayDestroyAPIView.as_view(), name="pay_delete"),

    #Subscrube
    path("subscribe/create/", SubscriptionCreateAPIView.as_view(), name="subscription_create"),
    path("subscribe/list/", SubscriptionListAPIView.as_view(), name="subscription_list"),
    path(
      "subscribe/deteil/<int:pk>/",
      SubscriptionRetrieveAPIView.as_view(),
      name="subscription_deteil",
    ),
    path(
      "subscribe/update/<int:pk>/",
      SubscriptionUpdateAPIView.as_view(),
      name="subscription_update",
    ),
    path(
      "subscribe/delete/<int:pk>/",
      SubscriptionDestroyAPIView.as_view(),
      name="subscription_delete",
    ),

] + router.urls

