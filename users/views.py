from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.views.generic import CreateView, UpdateView, ListView, FormView
from .models import User, Payment, Course
from .forms import RegisterForm, UserForm, ListUserForm, VerifyForm
# from .forms import UserProfileForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
import random
from config.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly, AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, PaymentSerializer
# from .serializers import RegisterUserSerializer
# from .permission import IsModerOrAuthor
# from .services import create_sprite_price, create_stripe_session
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import create_stripe_product, create_stripe_price, create_checkout_session


# from services import convert_rub_to_dollars


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('users:login')


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:verify')
    template_name = 'users/register.html'

    def get_success_message(self, cleaned_data):
        return f'Вам на почту отправлен код. Введите его для завершения регистрации.'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        code = ''.join(random.sample('0123456789', 4))
        new_user.verify_code = code
        new_user.is_active = False
        new_user.save()
        send_mail(
            'Верификация',
            f'Ваш код подтверждения: {code}',
            EMAIL_HOST_USER,
            [new_user.email],
            fail_silently=False,
        )
        self.request.session['user_id'] = new_user.id
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    """Контроллер страницы профиля"""
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """Отключаем необходимость получения pk, получая его из запроса"""
        return self.request.user


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер страницы списка пользователей"""
    model = User
    form_class = ListUserForm
    permission_required = 'users.view_user'


class VerifyUserView(FormView):
    form_class = VerifyForm
    template_name = 'users/verify.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user_id = self.request.session.get('user_id')
        if not user_id:
            messages.error(self.request, 'Ошибка. Попробуйте зарегистрироваться заново.')
            return redirect('users:register')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(self.request, 'Пользователь не найден.')
            return redirect('users:register')

        if user.verify_code == form.cleaned_data['code']:
            user.is_active = True
            user.verify_code = ''
            user.save()
            messages.success(self.request, 'Вы успешно подтвердили почту. Теперь вы можете войти.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Неправильный код подтверждения.')
            return self.form_invalid(form)


@permission_required('users.set_is_active')
def status_user(request, pk):
    """Контроллер смены статуса пользователя"""
    user = User.objects.get(pk=pk)
    if not user.is_superuser:
        if user.is_active is True:
            user.is_active = False
            user.save()
        elif user.is_active is False:
            user.is_active = True
            user.save()
        return redirect(reverse('users:user_list'))


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthorOrReadOnly]  # and; в одном лице


class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# ----------------------------------------------------------------------------------------------------------------------

# class PaymentCreateView(generics.CreateAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
#
#     def perform_create(self, serializer):
#         payment = serializer.save(user=self.request.user)
#         # amount_in_dollars = convert_rub_to_dollars(paymet.amount)
#         price = create_sprite_price(payment)
#         session_id, payment_link = create_stripe_session(price)
#         payment.session_id = session_id
#         payment.link = payment_link
#         payment.save()


class CreatePaymentView(APIView):
    def post(self, request, course_id):
        user = request.user

        course = get_object_or_404(Course, id=course_id)

        stripe_product = create_stripe_product(course.title)

        stripe_price = create_stripe_price(stripe_product['id'], int(course.price * 100))

        checkout_session = create_checkout_session(
            price_id=stripe_price['id'],
            success_url=settings.SUCCESS_URL,
            cancel_url=settings.CANCEL_URL,
        )

        payment = Payment.objects.create(
            course=course,
            stripe_product_id=stripe_product['id'],
            stripe_price_id=stripe_price['id'],
            stripe_session_id=checkout_session['id'],
            user=user,
        )
        payment.save()

        return Response({'checkout_url': checkout_session['url']})
