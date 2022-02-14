from django.db.models import fields
from rest_framework import serializers
from .models import Course
import random
import string


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
