from urllib.parse import uses_relative
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers 
import json 
from .models import Course, CourseUser, Video, VideoUser
from .serializers import CourseSerializers 
from django.db import connection
import jwt
from rest_framework.exceptions import AuthenticationFailed
from user.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.db import connection
from .serializers import *
from .models import User
import jwt
from datetime import *

def nothing():
        print("Nothing")


class CoursesView(APIView):
    def get(self, request):
        # 'data': json.loads(CourseSerializers('json', courses))
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,title,description,cover_img,total_videos,price FROM courses_course where status = 'active'")
        data = []
        for row in cursor.fetchall():
            # print(row)
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


class CourseDetailsView(APIView):
    def post(self,request):
        data = request.data
        course_id = data['course_id']
        course_details = Course.objects.filter(id=course_id).first()
        videos = Video.objects.filter(course_id=course_id).all()
        course_details = CourseSerializers(course_details)
        videos = VideoSerializers(videos, many=True)
        response = Response()
        response.data = {
            'course_details': course_details.data,
            'videos': videos.data
        }
        return response

class VideoListView(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        # user = User.objects.filter(id=payload['id']).first()
        cursor = connection.cursor()
        course_id = request.data['courseid']
        
        k = CourseUser.objects.filter(courseid=course_id,userid=payload['id']).first()
        if k is None:
            raise AuthenticationFailed('You are not enrolled in this course')

        cursor.execute("SELECT id,title,description,file FROM courses_video where course_id = %s and status = 'active'",[course_id])
        data = []
        
        for row in cursor.fetchall():
            video_user = VideoUser.objects.filter(videoid=row[0],userid=payload['id']).first()
            # print(f"\033[33m{row}")
            res = {}
            res['id'] = row[0]
            res['title'] = row[1]
            res['description'] = row[2]
            res['video_url'] = f"https://g4growth-courses.s3.amazonaws.com/courses/{row[3]}"
            res['is_watched'] = video_user.is_watched
            data.append(res)
        # print(data)
        return Response(data)

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

        return Response(serializer.data)


class MyCourse(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        mycourses = CourseUser.objects.filter(userid=payload['id'])
        print(payload['id'])
        serializer1 = CourseUserSerializers(mycourses, many=True)
        course_ids = []
        for courseUser in serializer1.data:
            course_ids.append(courseUser['courseid'])
            

        course_ids = list(set(course_ids))
        couses = Course.objects.filter(id__in=course_ids)

        # course_user = CourseUser.objects.filter(courseid=)

        serializer2 = CourseSerializers(couses, many=True)
        print(serializer2.data)

        for course in serializer2.data:
            for fields in serializer1.data:
                if course['id'] == fields['courseid']:
                    course['is_verified'] = fields['is_verified']
                    break
    
        data  = {
            "data": serializer2.data
        }
        print(data)

        return Response(data)

class VideoWatched(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        data = request.data
        print(data)
        video_id = data['video_id']
        video_user = VideoUser.objects.filter(videoid=video_id,userid=payload['id']).first()
        video_user.is_watched = True
        video_user.save()
        response =  Response()
        response.data = {
            "success" : True
        }
        return response 

def create_video_user(course_id,user_id):
    Q = f"SELECT `id` FROM courses_video where `course_id` ={course_id};"
    cursor  = connection.cursor()
    cursor.execute(Q)
    rows = cursor.fetchall()
    now  = datetime.now()
    for row in rows:
        Q2 = f"INSERT INTO `courses_videouser` ( `date_purchased`, `is_watched`, `userid_id`, `videoid_id`) VALUES ('{now}', '0', '{user_id}','{row[0]}');"
        print(Q2)
        cursor.execute(Q2)
        print("Insertion complete")
    cursor.close()
    return

def update_credit(userid, price):
        Q = f"SELECT * FROM `credit_referrer_referee` where `referee_id` = {userid};"
        try:
            cursor  = connection.cursor()
            cursor.execute(Q)
            rows = cursor.fetchall()
        except Exception as e:
            print(e)
            return
        print(f"{rows} rows found, length = {len(rows)}")
        if (len(rows) > 0):
            for row in rows:
                print(row)
                today = date.today()
                now = datetime.now()
                if (row[3] == 0):
                    amount = float(price) * float(0.533022015)
                    # Credit.objects.create(userid = row[1], amount = amount, referee = userid)
                    Q2 = f"INSERT INTO `credit_credit` ( `userid`,`date`, `amount`, `referee`) VALUES ('{row[1]}','{now}', '{amount}', '{userid}');"
                    print(Q2)
                    cursor.execute(Q2)
                    print("Credit Insertion complete")
                    # cursor.close()
                elif (row[3] == 1):
                    amount = float(price) * float(0.16611074)
                    # Credit.objects.create(userid = row[1], amount = amount, referee = userid)
                    Q2 = f"INSERT INTO `credit_credit` ( `userid`, `date`,`amount`, `referee`) VALUES ('{row[1]}','{now}', '{amount}', '{userid}');"
                    print(Q2)
                    cursor.execute(Q2)
                    print("Credit Insertion complete")
                    # cursor.close()
                elif (row[3] == 2):
                    # amount = float(price) * float(0.0993995997)
                    amount = 149
                    # Credit.objects.create(userid = row[1], amount = amount, referee = userid)
                    Q2 = f"INSERT INTO `credit_credit` ( `userid`, `date`,`amount`, `referee`) VALUES ('{row[1]}','{now}', '{amount}', '{userid}');"
                    print(Q2)
                    cursor.execute(Q2)
                    print("Credit Insertion complete")
                    # cursor.close()
        else:
            pass

class ProcessCreditView(APIView):

    def post(self,request):
        Q = "SELECT `courseid_id`,`userid_id` FROM courses_courseuser where `is_verified` = 1 and `is_processed` = 0;"
        print(Q)
        cursor  = connection.cursor()
        cursor.execute(Q)
        rows = cursor.fetchall()
        if (len(rows) > 0):
            print("FLAG\n")
            for row in rows:
                user_id =   row[1]
                course_id = row[0]
                course = Course.objects.get(id = course_id)
                price = course.price
                print(price,user_id,course_id)
                # print(course_id, user_id)
                create_video_user(course_id,user_id)
                update_credit(user_id,price)
            CourseUser.objects.filter(is_verified = True, is_processed = False).update(is_processed = True)
        else:
            nothing()
            pass
        response = Response()
        return response

        