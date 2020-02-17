from django.urls import path

from .views import (
    GroupAPIView,GroupRetrieveUpdateDeleteAPIView
)

app_name = 'groups'

urlpatterns = [
    path('',
         GroupAPIView.as_view(), name='group'),
    path('/<int:id>',
         GroupRetrieveUpdateDeleteAPIView.as_view(), name='group_views'),
]