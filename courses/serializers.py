from django.db.models import fields
from rest_framework import serializers
from .models import Course, CourseUser, Video, VideoUser
import random
import string


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseUser
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class VideoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = 'id','course','title','description'

class VideoUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = VideoUser
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance