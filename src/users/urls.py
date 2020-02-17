from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateDeleteAPIView,
     PasswordUpdateAPIView, HomeView, UserAPIView,ListUsersView
)

app_name = 'users'

urlpatterns = [
    path('', HomeView.as_view()),
    path('user/<int:id>', UserRetrieveUpdateDeleteAPIView.as_view(), name="current_user"),
    path('users', UserAPIView.as_view(), name='adduser'),
    path('users/all', ListUsersView.as_view(), name='signup'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/password_update/<token>',
         PasswordUpdateAPIView.as_view(), name='password_update'),
]