from django.http.response import FileResponse
from django.conf import settings
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import User
import jwt
import datetime
import random


class LoginView(APIView):
    def post(self, request):
        phoneno = request.data['phoneno']

        user = User.objects.filter(phoneno=phoneno).first()
        if user is None:
            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        user = User.objects.filter(phoneno=phoneno).first()

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        otp = LoginView.send_otp()
        referral_code = user.referral_id
        time = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        response.data = {
            'jwt': token,
            'otp': otp,
            'referral': referral_code,
            'time': time
        }
        user.otp = otp
        user.otp_validity = time
        user.save()

        return response

    def send_otp():
        otp = random.randint(100000, 999999)
        return otp


class OTPView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()

        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            raise AuthenticationFailed('Session time out! Try again!')

        otp = user.otp
        otp = str(otp)
        otp2 = request.data['otp']
        otp2 = str(otp2)
        if(user.otp_validity.replace(tzinfo=None) >= datetime.datetime.utcnow()):
            if(otp == otp2):
                response.data = {
                    'message': 'Succesfully logged in!'
                }
                user.is_logged = True
                user.save()
            else:
                if(not user.is_logged):
                    User.objects.filter(id=payload['id']).delete()
                response.delete_cookie('jwt')
                response.data = {
                    'message': 'Otp didn\'t match! Try again!'
                }
        else:
            if(not user.is_logged):
                User.objects.filter(id=payload['id']).delete()
            response.delete_cookie('jwt')
            response.data = {
                'message': 'Session time out! Try again!'
            }

        return response


class LogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()

        user = User.objects.filter(id=payload['id']).first()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You have successfully logged out!'
        }

        return response

class UserAPI(APIView):
    def get(self,request):
        # token = request.COOKIES.get('jwt')
        # print(token)
        # if not token:
        #     raise AuthenticationFailed('Unauthenticated')
        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        #     print(payload)
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed('Invalid')
        objectsmain=User.objects.all()
        serializer=ViewSerializer(objectsmain,many=True)
        return Response({'status':200,'message':serializer.data})
    
    
class EditAPI(APIView):
    def post(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid')
        try:
            objectsmain=User.objects.get(id=request.data['id'])
            if objectsmain:
                serializer=EditSerializer(objectsmain,data=request.data,partial=True)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'status':200,'message':serializer.errors})
            serializer.save()
            return Response({'status':200,'message':serializer.data})
        
        except Exception as ex:
            print(ex)
            return Response({'status':200,'message':'invalid id'})
