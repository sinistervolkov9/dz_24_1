from django.urls import path, include
from .apps import LmsConfig
from .views import (
    CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    LessonListView, LessonDetailView, LessonCreateView, LessonUpdateView, LessonDeleteView,
    CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
)
from rest_framework.routers import DefaultRouter

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/create/', CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    path('lessons/', LessonListView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),

    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),

]
