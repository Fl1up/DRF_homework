from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.users.models import User
from main.vehicle.models import Course, Lesson
from main.vehicle.serializers import SubscriptionSerializer


class LessonTests(APITestCase):
    def setUp(self):
        user = User.objects.create(email='testuser@mail.ru', password='testpass')
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=user)
        self.create_lesson = Lesson.objects.create(title='Вводный урок', course=self.course, url_video='https://www.youtube.com/@skypro-917')



    def test_create_lesson(self):
        response = self.client.post(
            '/lesson/create/',
            {'title': 'Вводный урок', 'course': self.course, 'video': 'https://www.youtube.com/@skypro-917'}
        )
        return response

    def test_get_lesson(self):
        response = self.client.get('/lesson/', )
        return response

    def test_retrieve_lesson(self):
        lesson = Lesson.objects.create(title='Вводный урок', course=self.course, url_video='https://www.youtube.com/@skypro-917')
        response = self.client.get(f'/Lesson/{lesson.id}/')
        self.assertEqual(response.status_code, 200)


    def test_update_lesson(self):
        course = Course.objects.create(title='Some course')
        lesson = Lesson.objects.create(title='Some title', description='Some description', course=course)
        response = self.client.patch(f'/Lesson/update/{course.id}/',
                                     {'title': '1 урок', 'course': course.id,
                                      'video': 'https://www.youtube.com/@skypro-916'}
                                     )
        self.assertEqual(response.status_code, 200)

    def delete_lesson(self, lesson_id):
        return self.client.delete(f'/lesson/delete/{lesson_id}/', )


# class SubscriptionTests(APITestCase):
#     def setUp(self):
#         self.course = Course.objects.create(title='Test Course', description='This is a test course')
#         self.subscription = SubscriptionSerializer.objects.create(course=self.course, email='test@test.com')
#
#     def test_create_subscription(self):
#         url = reverse('subscription-list')
#         data = {'course': self.course.id, 'email': 'new@test.com'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(SubscriptionSerializer.objects.count(), 2)
#         self.assertEqual(SubscriptionSerializer.objects.last().email, 'new@test.com')
#
#     def test_retrieve_subscription(self):
#         url = reverse('subscription-detail', args=[self.subscription.id])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['email'], 'test@test.com')
#
#     def test_update_subscription(self):
#         url = reverse('subscription-detail', args=[self.subscription.id])
#         data = {'email': 'updated@test.com'}
#         response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.subscription.refresh_from_db()
#         self.assertEqual(self.subscription.email, 'updated@test.com')
#
#     def test_delete_subscription(self):
#         url = reverse('subscription-detail', args=[self.subscription.id])
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(SubscriptionSerializer.objects.count(), 0)
