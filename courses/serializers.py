from django.db.models import fields
from rest_framework import serializers
from .models import Course, CourseUser, Video, VideoUser
import random
import string


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class VideoListViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'description', 'file']
