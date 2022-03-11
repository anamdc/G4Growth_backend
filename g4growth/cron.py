import datetime
from user.models import User
from courses.models import CourseUser,Video,VideoUser,Course
from credit.models import Credit,Referrer_referee
from django.db import connection



def delete_expired():
    print("delete expired by cronrule")
    User.objects.filter(otp_validity__lt=datetime.datetime.utcnow(), is_verified = False).delete()

