from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.vehicle.models import Course, CourseSubscription
from main.vehicle.serializers import SubscriptionSerializer


class VehicleTestCase(APITestCase):
    def setUp(self):
        pass

    def test_create_course(self):
            """ тест на создание курса """
            data = {
                "title": "test",
                "description": "test"
            }
            response = self.client.post(
                "/Course/",
                data=data
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED
            )

            self.assertEqual(
                response.json(),
                {'id': 1, 'lessons_information': [], 'lessons': [], 'lessons_count': 0, 'subscribed': False,
                 'title': 'test', 'preview': None, 'description': 'test', 'owner': None}
            )

            self.assertTrue(
                Course.objects.all().exists()
            )

    def test_list_course(self):
        """ тест на лист курса  """
        Course.objects.create(
            title="list test",
            description="list test"
        )

        response = self.client.post(
            "/Course/",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': 2, 'lessons_information': [], 'lessons': [], 'lessons_count': 0, 'subscribed': False,
             'title': 'list test', 'preview': None, 'description': 'list test', 'owner': None}
        )


