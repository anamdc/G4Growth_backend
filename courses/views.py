from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
import json 
from .models import Course
from .serializers import CourseSerializers 
from django.db import connection



class CoursesView(APIView):
    def get(self, request):
                    # 'data': json.loads(CourseSerializers('json', courses))
        cursor = connection.cursor()
        cursor.execute("SELECT id,title,description,cover_img,total_videos,price FROM courses_course where status = 'active'")
        data = []
        for row in cursor.fetchall():
            print(row)
            res = {}
            res['id'] = row[0]
            res['title'] = row[1]
            res['description'] = row[2]
            res['cover_img'] = "https://g4growth-courses.s3.amazonaws.com/courses/public/" + row[3]
            res['total_videos'] = row[4]
            res['price'] = row[5]
            data.append(res)
        response = Response()
        response.data = {
            'data': data
        }
        return response
