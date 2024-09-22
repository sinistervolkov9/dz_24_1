from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CourseForm, LessonForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Course, Lesson, Subscription
from users.models import Payment
from django.urls import reverse_lazy
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from .serializers import CourseSerializer, LessonSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.permission import IsModerOrAuthor, IsPaymet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .paginators import Pagination
from .send_mails_service import send_update_mail
# from django.shortcuts import redirect
# from django.contrib import messages
# from django.conf import settings
# import stripe
#
# stripe.api_key = settings.STRIPE_SECRET_KEY


# class PaymentPageView(DetailView):
#     model = Course
#     template_name = 'lms/payment_page.html'
#     context_object_name = 'course'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         course = self.get_object()
#
#         price_id = 'your_stripe_price_id_here'
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price': price_id,
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             success_url=settings.SUCCESS_URL,
#             cancel_url=settings.CANCEL_URL,
#         )
#
#         context['checkout_session_id'] = session.id
#         return context


# ----------------------------------------------------------------------------------------------------------------------

class CourseListView(ListView):
    model = Course
    template_name = 'lms/course_list.html'
    context_object_name = 'course_list'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'lms/course_detail.html'
    context_object_name = 'course'

    # def get(self, request, *args, **kwargs):
    #     course = self.get_object()
    #
    #     if not Payment.objects.filter(user=request.user, course=course, status='success').exists():
    #         messages.error(request, 'Вы не оплатили этот курс. Пожалуйста, оплатите для доступа.')
    #         print('NO')
    #         print(course.id)
    #         return redirect('payment_page', course_id=course.id)
    #
    #     return super().get(request, *args, **kwargs)

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
        send_update_mail(self.object)
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
    pagination_class = Pagination

    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticatedOrReadOnly, IsPaymet]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsModerOrAuthor]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsModerOrAuthor]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsModerOrAuthor]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


# ----------------------------------------------------------------------------------------------------------------------

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = Pagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsModerOrAuthor]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsModerOrAuthor]
        else:
            permission_classes = [IsAuthenticated, IsModerOrAuthor]

        return [permission() for permission in permission_classes]


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


# ----------------------------------------------------------------------------------------------------------------------

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course']
    # ordering_fields = ['payment_date']
    # ordering = ['-payment_date']


# ----------------------------------------------------------------------------------------------------------------------

class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)  # Проверка на подписку

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message})
