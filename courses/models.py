from pyexpat import model
from django.db import models
from user.models import User
from g4growth.storage_backends import MediaStorage, PublicMediaStorage
# Create your models here.
status_choices = (('active', 'ACTIVE'), ('inactive',
                  'INACTIVE'), ('deleted', 'DELETED'))


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    title = models.CharField(max_length=50)
    description = models.TextField()
    cover_img = models.FileField(
        storage=PublicMediaStorage, blank=True, null=True)
    status = models.CharField(
        max_length=8, choices=status_choices, default='active')
    total_videos = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank= True)
    file = models.FileField(storage=MediaStorage, blank=True, null=True)
    status = models.CharField(
        max_length=8, choices=status_choices, default='active')

    def __str__(self):
        return str(self.course) + '>' + str(self.title)


class VideoUser(models.Model):
    id = models.AutoField(primary_key=True)
    videoid = models.ForeignKey(Video, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)
    is_watched = models.BooleanField(default=False)

    def __str__(self):
        return str(self.userid) + '&' + str(self.videoid)


class CourseUser(models.Model):
    id = models.AutoField(primary_key=True)
    courseid = models.ForeignKey(Course, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)
    percentage = models.IntegerField(default=0)
    payment_ss = models.ImageField(
        storage=PublicMediaStorage, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    def __str__(self):
        return str(self.userid) + '&' + str(self.courseid)
