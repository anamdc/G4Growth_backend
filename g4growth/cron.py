import datetime
from user.models import User
from courses.models import CourseUser,Video,VideoUser,Course
from credit.models import Credit,Referrer_referee


def create_video_user(courseid,userid):
    videolist = Video.objects.filter(courseid = courseid)
    for video in videolist:
        VideoUser.objects.create(userid = userid, videoid = video.id, is_completed = False)

def update_credit(userid,price):
    referrers = Referrer_referee.objects.filter(referrer_id = userid)
    if (len(referrers) > 0):
        for referrer in referrers:
            if (referrer.level == False):
                amount = price * 0.02
                Credit.objects.create(userid = referrer.referee_id, amount = amount, referee = userid)
            elif ( referrer.level == True):
                amount = price * 0.05
                Credit.objects.create(userid = referrer.referee_id, amount = amount, referee = userid)
    else:
        pass



def delete_expired():
    print("delete expired by cronrule")
    User.objects.filter(otp_validity__lt=datetime.datetime.utcnow(), is_verified = False).delete()

def add_credit():
    print("credit added by cronrule")
    orders = CourseUser.objects.filter(is_verified = True, is_processed = False)
    if (len(orders) >0):
        for order in orders:
            user_id = order.userid
            course_id = order.courseid
            course = Course.objects.get(id = course_id)
            price = course.price
            create_video_user(course_id,user_id)
            update_credit(user_id,price)
        CourseUser.objects.filter(is_verified = True, is_processed = False).update(is_processed = True)
    else:
        pass