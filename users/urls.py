from django.urls import path
from .apps import UsersConfig
from .views import UserLoginView, UserLogoutView, UserUpdateView, UserListView, status_user, RegisterUserView, VerifyUserView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('logout/', UserLogoutView.as_view(http_method_names=['get', 'post', 'options']), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify/', VerifyUserView.as_view(), name='verify'),

    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('status_user/<int:pk>', status_user, name='status_user'),
]
