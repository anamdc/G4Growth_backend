from django.urls import path
# from .views import LoginView, OTPView, LogoutView
from .views import CoursesView, VideoListView, PurchaseView

urlpatterns = [
    path('courseslist', CoursesView.as_view()),
    path('videolist', VideoListView.as_view()),
    path('purchase', PurchaseView.as_view()),
]
