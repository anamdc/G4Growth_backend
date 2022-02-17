from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers 
import json 
from .models import Course, CourseUser, Video, VideoUser
from .serializers import CourseSerializers , VideoListViewSerializers
from django.db import connection
import jwt
from rest_framework.exceptions import AuthenticationFailed
from user.models import User


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

class VideoListView(APIView):
    def post(self,request):
        # token = request.COOKIES.get('jwt')

        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Token Expired! Log in again.')

        # user = User.objects.filter(id=payload['id']).first()
        course_id = request.data['course_id']
        videos = Video.objects.filter(course=course_id).all()
        print(videos)
        result = VideoListViewSerializers(videos)
        print(result.data)
        return Response(result.data)