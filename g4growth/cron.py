import datetime
from user.models import User
from courses.models import CourseUser,Video,VideoUser,Course
from credit.models import Credit,Referrer_referee
from django.db import connection

# def create_video_user(courseid,userid):
#     videolist = Video.objects.filter(course = courseid)
#     for video in videolist:
#         VideoUser.objects.create(userid = userid, videoid = video.id, is_completed = False)

def create_video_user(course_id,user_id):
    Q = f"SELECT `id` FROM courses_video where `course_id` ={course_id};"
    cursor  = connection.cursor()
    cursor.execute(Q)
    rows = cursor.fetchall()
    now  = datetime.datetime.now()
    for row in rows:
        Q2 = f"INSERT INTO `courses_videouser` ( `date_purchased`, `is_watched`, `userid_id`, `videoid_id`) VALUES ('{now}', '0', '{user_id}','{row[0]}');"
        cursor.execute(Q2)


# def update_credit(userid,price):
#     referrers = Referrer_referee.objects.filter(referrer_id = userid)
#     if (len(referrers) > 0):
#         for referrer in referrers:
#             if (referrer.level == False):
#                 amount = price * 0.02
#                 Credit.objects.create(userid = referrer.referee_id, amount = amount, referee = userid)
#             elif ( referrer.level == True):
#                 amount = price * 0.05
#                 Credit.objects.create(userid = referrer.referee_id, amount = amount, referee = userid)
#     else:
#         pass

def update_credit(userid, price):
    Q = f"SELECT * FROM `credit_referrer_referee` where `referee_id` = {userid};"
    cursor  = connection.cursor()
    cursor.execute(Q)
    rows = cursor.fetchall()
    print(rows)
    if (len(rows) > 0):
        for row in rows:
            print(row)
            if (row[2] == False):
                amount = price * 0.02
                # Credit.objects.create(userid = row[1], amount = amount, referee = userid)
            elif (row[2] == True):
                amount = price * 0.05
                # Credit.objects.create(userid = row[1], amount = amount, referee = userid)
            Q2 = f"INSERT INTO `credit_credit` ( `userid_id`, `amount`, `referee`) VALUES ('{row[1]}', '{amount}', '{userid}');"
            cursor.execute(Q2)
    else:
        pass

def delete_expired():
    print("delete expired by cronrule")
    User.objects.filter(otp_validity__lt=datetime.datetime.utcnow(), is_verified = False).delete()

def add_credit():
    Q = "SELECT `courseid_id`,`userid_id` FROM courses_courseuser where `is_verified` = 1 and `is_processed` = 0;"
    cursor  = connection.cursor()
    cursor.execute(Q)
    rows = cursor.fetchall()
    if (len(rows) > 0):
        for row in rows:
            user_id =   row[1]
            course_id = row[0]
            course = Course.objects.get(id = course_id)
            price = course.price
            print(price)
            # print(course_id, user_id)
            create_video_user(course_id,user_id)
            update_credit(user_id,price)
        CourseUser.objects.filter(is_verified = True, is_processed = False).update(is_processed = True)
    else:
        pass