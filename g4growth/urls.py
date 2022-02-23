from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/courses/', include('courses.urls')),
    path('creditapi/', include('credit.urls')),
]

