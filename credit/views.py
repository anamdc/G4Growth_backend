from urllib.parse import uses_relative
# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers 
import json 
from .models import Credit, Referrer_referee
#from .serializers import *
from django.db import connection
import jwt
from rest_framework.exceptions import AuthenticationFailed
from user.models import User
import datetime
from user.views import *

class EarningStatus(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')
        response=Response()


        user = Credit.objects.filter(userid=payload['id'])#id is userid incredit model
        user1 = User.objects.filter(id= payload['id']).first()
        referral_count=len(Referrer_referee.objects.filter(referrer_id = user1.id))
        if user:
            #self.start=user[0].date
            day=datetime.date.today().weekday()
            total=0
            monthlyincome=0
            weeklyincome=0
            todayincome=0
            for i in range(len(user)):
                total+=user[i].amount
                if str(datetime.date.today())[5:7]==str(user[i].date)[5:7]:
                    monthlyincome+=user[i].amount
                    if int(str(datetime.date.today())[8:10])-int(str(user[i].date)[8:10])<=day:
                        weeklyincome+=user[i].amount
                if datetime.date.today()==user[i].date:
                    todayincome+=user[i].amount
                # else:
                #     self.todayincome+=user[i].amount#same weekly,monthly korte hoibo
            
        #serializer = CreditSerializer(user)
            response.data = {
                'user-id': payload['id'],
                'todays_income': todayincome,
                'weekly_income': weeklyincome,
                'monthly_income': monthlyincome,
                'total_income':total,
                'referral_count': referral_count,
            }
        else:
            response.data = {
                'user-id': payload['id'],
                'todays_income': 0,
                'weekly_income': 0,
                'monthly_income': 0,
                'total_income':0,
                'referral_count': 0,
            }
              
        return response
        # else:
        #     return Response(serializer.data)#date ?? 


