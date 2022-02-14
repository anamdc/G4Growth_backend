from django.urls import path
from .views import LoginView, OTPView, LogoutView,UserAPI,EditAPI

urlpatterns = [
    path('login', LoginView.as_view()),
    path('otp', OTPView.as_view()),
    path('logout', LogoutView.as_view()),
    path('viewprofile',UserAPI.as_view()),
    path('editprofile',EditAPI.as_view()),
]
