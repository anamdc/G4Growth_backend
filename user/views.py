from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from credit.models import Referrer_referee
from .serializers import *
from .models import User
import jwt
import datetime
import random
from django.db import connection
import urllib

apik="NTM3MzY2NTI1OTc1NzM1ODM4NmU3NTMwNDEzMTZjNTg="
sendern="BOOKRO"

def sentOTP(apikey,numbers,sender,message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    print(fr)
    return True

class LoginView(APIView):
    def post(self, request):
        phoneno = request.data['phoneno']
        referrer_id = request.data['referrer_id']

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

        token = jwt.encode(payload, 'secret00', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        otp = LoginView.send_otp()
        referral_code = user.referral_id
        time = datetime.datetime.utcnow() + datetime.timedelta(seconds=240)
            #         'jwt': token,
            # 'otp': otp,
        response.data = {
            'referral': referral_code,
            'time': time,
        }
        template = f"Your Login OTP for Bookkaaro is {otp}. Please do not share this with anyone."
        sentOTP(apik,phoneno,sendern,template)
        user.otp = otp
        user.otp_validity = time
        user.referrer_id = referrer_id
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
            payload = jwt.decode(token, 'secret00', algorithms=['HS256'])
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
        cursor = connection.cursor()
        if(user.otp_validity.replace(tzinfo=None) >= datetime.datetime.utcnow()):
            if(otp == otp2):
                payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=432000),
                    'iat': datetime.datetime.utcnow(),
                }
                token = jwt.encode(payload, 'secret', algorithm='HS256')
                response.set_cookie(key='jwt', value=token, httponly=True)
                if not user.is_verified:
                    if user.referrer_id:
                        referrer_1 = User.objects.filter(
                            referral_id=user.referrer_id).first()
                        if not referrer_1:
                            response.delete_cookie('jwt')
                            cursor.close()
                            response.data = {
                                'message': 'Wrong referrer ID, try again!'
                            }
                        else:
                            user.is_verified = True
                            user.save()
                            response.data = {
                                'message': 'Succesfully logged in!'
                            }
                            query1 = f"Insert INTO credit_referrer_referee (referrer_id, referee_id, level) VALUES ({referrer_1.id}, {user.id}, 0)"
                            print(query1)
                            cursor.execute(query1)

                            if referrer_1.referrer_id:
                                referrer_2 = User.objects.filter(
                                    referral_id=referrer_1.referrer_id).first()
                                # print(query2)
                                query2 = f"Insert INTO credit_referrer_referee (referrer_id, referee_id, level) VALUES ({referrer_2.id}, {user.id}, 1)"
                                cursor.execute(query2)

                                if referrer_2.referrer_id:
                                    referrer_3 = User.objects.filter( referral_id=referrer_2.referrer_id).first()
                                    query3 = f"Insert INTO credit_referrer_referee (referrer_id, referee_id, level) VALUES ({referrer_3.id}, {user.id}, 2)"
                                    print(query3)
                                    cursor.execute(query3)
                                    cursor.close()
                                else:
                                    cursor.close()
                            else:
                                cursor.close()
                    else:
                        user.is_verified = True
                        user.save()
                        response.data = {
                            'message': 'Succesfully logged in!'
                        }
                else:
                    user.is_verified = True
                    user.save()
                    response.data = {
                        'message': 'Succesfully logged in!'
                    }
            else:
                if(not user.is_verified):
                    User.objects.filter(id=payload['id']).delete()
                response.delete_cookie('jwt')
                response.data = {
                    'message': 'Otp didn\'t match! Try again!'
                }
        else:
            if(not user.is_verified):
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


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        print(token)
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializers(user)


        referees = Referrer_referee.objects.filter(
            referrer_id=user.id)
        l = len(referees)
        response = Response()
        response.data = {
            'user': serializer.data,
            'referees': l
        }
        return response


        # return Response(serializer.data)


class UpdateView(APIView):
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

        try:
            name = request.data['name']
        except:
            name = user.name

        try:
            bank_name = request.data['bank_name']
        except:
            bank_name = user.bank_name

        try:
            account_no = request.data['account_no']
        except:
            account_no = user.account_no

        try:
            ifsc_code = request.data['ifsc_code']
        except:
            ifsc_code = user.ifsc_code

        try:
            email = request.data['email']
        except:
            email = user.email

        try:
            profile_img = request.data['profile_img']
        except:
            profile_img = user.profile_img

        user.name = name
        user.bank_name = bank_name
        user.ifsc_code = ifsc_code
        user.email = email
        user.account_no = account_no
        user.profile_img = profile_img
        user.save()

        response.data = {
            'message': 'Profile successfully updated!'
        }
        return response

class AuthenticationCheck(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')
        response = Response()
        response.data = {
            'message': 'You are authenticated!'
        }
        return response
