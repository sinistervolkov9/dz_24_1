from django.urls import path, include
from .apps import UsersConfig
from .views import UserLoginView, UserLogoutView, UserUpdateView, UserListView, status_user, RegisterUserView, \
    VerifyUserView, CreatePaymentView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('logout/', UserLogoutView.as_view(http_method_names=['get', 'post', 'options']), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify/', VerifyUserView.as_view(), name='verify'),

    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('status_user/<int:pk>', status_user, name='status_user'),

    path('', include(router.urls)),

    path('register_user/', UserCreateView.as_view(), name='user_register'),

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('payment/', PaymentCreateView.as_view(), name='payment'),
    path('courses/<int:course_id>/create-payment/', CreatePaymentView.as_view(), name='create_payment'),
]
