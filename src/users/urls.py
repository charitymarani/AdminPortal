from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView,
     PasswordUpdateAPIView, HomeView
)

app_name = 'authentication'

urlpatterns = [
    path('', HomeView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="current_user"),
    path('users/', RegistrationAPIView.as_view(), name='signup'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/password_update/<token>',
         PasswordUpdateAPIView.as_view(), name='password_update'),
]