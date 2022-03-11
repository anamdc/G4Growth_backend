import datetime
from user.models import User
from courses.models import CourseUser,Video,VideoUser,Course
from credit.models import Credit,Referrer_referee
from django.db import connection
import http.client


def delete_expired():
    print("delete expired by cronrule")
    User.objects.filter(otp_validity__lt=datetime.datetime.utcnow(), is_verified = False).delete()

def add_credit():
    print("credit added")
    
    conn = http.client.HTTPSConnection("api.g4growth.com")
    payload = ''
    conn.request("POST", "/api/courses/process-credit", payload)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))