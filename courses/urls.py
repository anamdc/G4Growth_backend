from django.urls import path
# from .views import LoginView, OTPView, LogoutView
from .views import CoursesView

urlpatterns = [
    path('courseslist', CoursesView.as_view()),
]