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
        referral_id = request.data['referral_id']

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
        user.referrer_id = referral_id
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
                user.is_verified = True
                user.save()
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

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializers(user)

        return Response(serializer.data)


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
