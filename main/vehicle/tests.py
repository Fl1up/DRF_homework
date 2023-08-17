from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.users.models import User
from main.vehicle.models import Course, Subscription, Pay, Lessons
from main.vehicle.serializers import SubscriptionSerializer


class LessonTestsCase(APITestCase):
    def setUp(self):
        user = User.objects.create(email='testuser@mail.ru', password='testpass')
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=user)
        self.create_lesson = Lessons.objects.create(title='Вводный урок', course=self.course,
                                                   url_video='https://www.youtube.com/@skypro-917')

    def test_create_lesson(self):
        response = self.client.post(
            '/Lesson/create/',
            {'title': 'Вводный урок', 'course': self.course, 'video': 'https://www.youtube.com/@skypro-917'}
        )
        return response

    def test_get_lesson(self):
        response = self.client.get('/Lesson/', )
        return response

    def test_retrieve_lesson(self):
        lesson = Lessons.objects.create(title='Вводный урок', course=self.course,
                                       url_video='https://www.youtube.com/@skypro-917')
        response = self.client.get(f'/Lesson/{lesson.id}/')
        self.assertEqual(response.status_code, 200)

    def test_update_lesson(self):
        course = Course.objects.create(title='Some course')
        lesson = Lessons.objects.create(title='Some title', description='Some description', course=course)
        response = self.client.patch(f'/Lesson/update/{course.id}/',
                                     {'title': '1 урок', 'course': course.id,
                                      'video': 'https://www.youtube.com/@skypro-916'}
                                     )
        self.assertEqual(response.status_code, 200)

    def delete_lesson(self, lesson_id):
        return self.client.delete(f'/lesson/delete/{lesson_id}/', )


class CourseSubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@mail.ru', password='testpass')
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

    def test_create_subscription(self):
        response = self.client.post(
            f'Courses/{self.course.id}/subscribe/',
            {'title': 'Вводный урок', 'course': self.course, 'video': 'https://www.youtube.com/@skypro-917'}
        )
        return response


class PayTestCase(APITestCase):
    def setUp(self) -> None:
        """Общие данные"""

        self.user = User.objects.create(
            email="3@admin.ru", password="123", is_active=True
        )
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.pay_test = Pay.objects.create(
            id=2,
            pay_date='2099-08-06"',
            pay_sum=15,
            payment_type="CASH",
            user=self.user,
        )

    def test_create_pay(self):
        """Создание курса тест"""

        data = {
            "id": 1,
            "pay_sum": 2000,
            "payment_type": "Card",
            "user": 1,
            "course_name": 1
        }

        response = self.client.post("/payment/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Pay.objects.all().exists())  # нахождение в базе

    def test_list_pay(self):
        """Вывод всех оплат тест"""
        responce = self.client.get("/payment/list/")

        data = {
            {
                "count": 3,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "pay_date": "2023-08-17",
                        "pay_sum": 2500,
                        "payment_type": "Card",
                        "user": 1,
                        "course_name": 1,
                        "lesson": 1
                    },
                ],
            }
        }

        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.json(), data)

    def test_detail_pay(self):
        """Вывод одной оплаты тест"""
        response = self.client.get("/payment/deteil/2/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_pay(self):
        """Тест обновления оплаты"""
        data = {
            "pay_sum": 150,
            "pay_date": "2023-08-12",
            "payment_type": "CASH",
            "user": self.user.id,
        }

        response = self.client.put("/payment/update/2/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_pay(self):
        """Тест удаления оплаты"""
        response = self.client.delete("/payment/delete/2/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
