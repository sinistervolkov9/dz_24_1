from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CourseForm, LessonForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course, Lesson
from users.models import Payment
from django.urls import reverse_lazy
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from .serializers import CourseSerializer, LessonSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PaymentSerializer


class CourseListView(ListView):
    model = Course
    template_name = 'lms/course_list.html'
    context_object_name = 'course_list'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'lms/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = self.object.lesson.all()
        return context


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'lms/course_form.html'
    # fields = ['title', 'preview', 'description']
    success_url = reverse_lazy('lms:course_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'lms/course_form.html'
    success_url = reverse_lazy('lms:course_list')

    def form_valid(self, form):
        print('fv')
        form.instance.user = self.request.user
        # form.save()
        response = super().form_valid(form)

        return response

    def get_success_url(self):
        return reverse_lazy('lms:course_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        course = self.get_object()
        return self.request.user == course.user or self.request.user.is_superuser


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'lms/course_confirm_delete.html'
    success_url = reverse_lazy('lms:course_list')

    def test_func(self):
        course = self.get_object()
        return self.request.user == course.user or self.request.user.is_superuser


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# ----------------------------------------------------------------------------------------------------------------------

class LessonListView(ListView):
    model = Lesson
    template_name = 'lms/lesson_list.html'
    context_object_name = 'lessons'


class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lms/lesson_detail.html'
    context_object_name = 'lesson'


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lms/lesson_form.html'

    def get_success_url(self):
        return reverse_lazy('lms:course_detail', kwargs={'pk': self.object.course.pk})


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lms/lesson_form.html'
    # fields = ['title', 'description', 'preview', 'video_url', 'course']
    success_url = reverse_lazy('lms:lesson_detail')

    def get_success_url(self):
        return reverse_lazy('lms:lesson_detail', kwargs={'pk': self.object.pk})


class LessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lesson
    template_name = 'lms/lesson_confirm_delete.html'
    success_url = reverse_lazy('lms:course_list')

    def test_func(self):
        lesson = self.get_object()
        return self.request.user.is_superuser or lesson.user == self.request.user


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = LessonSerializer


# ----------------------------------------------------------------------------------------------------------------------

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']