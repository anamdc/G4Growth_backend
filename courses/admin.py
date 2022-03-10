from django.contrib import admin
from .models import Course, Video, VideoUser,CourseUser
# # Register your models here.
# admin.site.register(Course)
# admin.site.register(Video)
# admin.site.register(VideoUser)
# admin.site.register(CourseUser)
# Register your models here.

@admin.register(Course)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'total_videos', 'price', 'status')

@admin.register(Video)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title', 'status')

@admin.register(VideoUser)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'videoid', 'userid', 'is_watched')

@admin.register(CourseUser)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'courseid', 'userid', 'is_verified', 'is_processed')