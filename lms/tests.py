from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from lms.models import Lesson, Course, Subscription
from django.contrib.auth import get_user_model


class LessonCRUDTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user', email='testuser@example.com', password='password123'
        )
        cls.course = Course.objects.create(
            title="Test Course", description="Test course description", user=cls.user
        )
        cls.lesson_data = {
            "title": "Test Lesson",
            "description": "Lesson description",
            "video_url": "https://www.youtube.com/watch?v=Lqrdps0doSo&t=1524s&ab_channel=BobbyNsenga"
        }

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        response = self.client.post(reverse('api:lesson-list'), self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_lesson_list(self):
        response = self.client.get(reverse('api:lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(title="Old Lesson", user=self.user)
        updated_data = {"title": "Updated Lesson"}
        response = self.client.patch(reverse('api:lesson-detail', args=[lesson.id]), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get(id=lesson.id).title, "Updated Lesson")

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(title="Delete Lesson", user=self.user)
        response = self.client.delete(reverse('api:lesson-detail', args=[lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='user', email='testuser@example.com', password='password123'
        )
        cls.course = Course.objects.create(
            title="Test Course", description="Test course description", user=cls.user
        )
        cls.lesson_data = {
            "title": "Test Lesson",
            "description": "Lesson description",
            "course": cls.course.id
        }

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        response = self.client.post(reverse('lms:subscribe'), {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):

        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(reverse('lms:subscribe'), {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
