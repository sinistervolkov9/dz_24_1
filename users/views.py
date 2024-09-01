from django.contrib.auth.views import LoginView, LogoutView
# from django.core.mail import send_mail
from django.views.generic import CreateView, UpdateView, ListView, FormView
from .models import User
from .forms import RegisterForm, UserForm, ListUserForm, VerifyForm
# from .forms import UserProfileForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
import random
# from config.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('newsletter:base')


# class RegisterUserView(SuccessMessageMixin, CreateView):
#     model = User
#     form_class = RegisterForm
#     success_url = reverse_lazy('users:login')
#     template_name = 'users/register.html'
#
#     def get_success_message(self, cleaned_data):
#         return f'Вам на почту отправлен код. Введите его для завершения регистрации'
#
#     def form_valid(self, form):
#         """Верификация по ссылке через почту"""
#         new_user = form.save()
#         code = ''.join(random.sample('0123456789', 4))
#         new_user.verify_code = code
#         new_user.is_active = False
#         send_mail(
#             'Верификация',
#             f'Перейдите по ссылке для верификации: '
#             f'http://127.0.0.1:8000/users/verification/{code}',
#             EMAIL_HOST_USER,
#             [new_user.email]
#         )
#         return super().form_valid(form)


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
        # send_mail(
        #     'Верификация',
        #     f'Ваш код подтверждения: {code}',
        #     EMAIL_HOST_USER,  # замените на ваш EMAIL_HOST_USER
        #     [new_user.email],
        #     fail_silently=False,
        # )
        # self.request.session['user_id'] = new_user.id
        return super().form_valid(form)


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


# def verification(request, code):
#     """Контроллер подтверждения верификации"""
#     user = User.objects.get(verify_code=code)
#     user.is_active = True
#     user.save()
#     return redirect(reverse('users:login'))


# class ProfileView(UpdateView):
#     model = User
#     form_class = UserProfileForm
#     success_url = reverse_lazy('user:profile')
#     extra_context = {'title': 'Профиль'}
#
#     def get_object(self, queryset=None):
#         return self.request.user


class UserUpdateView(UpdateView):
    """Контроллер страницы профиля"""
    model = User
    form_class = UserForm
    success_url = reverse_lazy('newsletter:base')

    def get_object(self, queryset=None):
        """Отключаем необходимость получения pk, получая его из запроса"""
        return self.request.user


def generate_password(request):
    """Контроллер смены пароля и отправка сгенерированного пароля на почту"""
    new_password = User.objects.make_random_password()
    request.user.set_password(new_password)
    request.user.save()
    # send_mail(
    #     'Смена пароля',
    #     f'Ваш новый пароль для авторизации: {new_password}',
    #     EMAIL_HOST_USER,
    #     [request.user.email]
    # )
    # messages.success(request,
    #                  'Вам на почту отправлено письмо '
    #                  'с новым паролем для вашего аккаунта')
    return redirect(reverse('users:login'))


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер страницы списка пользователей"""
    model = User
    form_class = ListUserForm
    permission_required = 'users.view_user'


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
