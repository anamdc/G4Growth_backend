from django.urls import path
from .views import LoginView, OTPView, LogoutView, UserView, UpdateView, AuthenticationCheck

urlpatterns = [
    path('login', LoginView.as_view()),
    path('otp', OTPView.as_view()),
    path('logout', LogoutView.as_view()),
    path('viewprofile', UserView.as_view()),
    path('editprofile', UpdateView.as_view()),
    path('userauth', AuthenticationCheck.as_view())
]
