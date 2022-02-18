from urllib.parse import uses_relative
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.db import connection
from .serializers import *
from .models import User
import jwt
import datetime


class CoursesView(APIView):
    def get(self, request):
        # 'data': json.loads(CourseSerializers('json', courses))
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,title,description,cover_img,total_videos,price FROM courses_course where status = 'active'")
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


class PurchaseView(APIView):
    def post(self, request):

        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        print(request.data, type(request.data))

        serializer = CourseUserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return(serializer.data)
