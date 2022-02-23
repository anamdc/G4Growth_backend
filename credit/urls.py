from django.urls import path
from .views import EarningStatus

urlpatterns = [
    path('status', EarningStatus.as_view()),
]