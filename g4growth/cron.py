import datetime
from user.models import User


def delete_expired():
    User.objects.filter(otp_validity__lt=datetime.datetime.utcnow()).delete()
