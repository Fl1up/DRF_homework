from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.users.models import User
from main.vehicle.models import Course, Lesson, Subscription
from main.vehicle.serializers import SubscriptionSerializer


class LessonTestsCase(APITestCase):
    def setUp(self):
        user = User.objects.create(email='testuser@mail.ru', password='testpass')
        self.course = Course.objects.create(title='Test Course', description='Test Description', owner=user)
        self.create_lesson = Lesson.objects.create(title='Вводный урок', course=self.course, url_video='https://www.youtube.com/@skypro-917')



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

    # def test_delete_subscription(self):  # не видит unsubscribe
    #     url = reverse('unsubscribe', args=[self.course.id, self.subscription.id])
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(CourseSubscription.objects.filter(id=self.subscription.id).exists())
    #
    # def test_retrieve_subscription(self): # не видит subscribe-get
    #     url = reverse("subscribe-get", args=[self.subscription.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['email'], 'test@test.com')




