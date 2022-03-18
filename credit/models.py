from datetime import date
from django.db import models

# Create your models here.
class Credit(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.IntegerField()
    date = models.DateField(default=date.today)
    amount = models.IntegerField()
    referee = models.IntegerField()

    def __str__(self):
        return str(self.userid)

class Referrer_referee(models.Model):
    referrer_id = models.CharField(max_length=9, blank=True)
    referee_id = models.CharField(max_length=9, blank=True)
    level = models.IntegerField(default=0)

    def __str__(self):
        return str(self.referrer_id) + " " + str(self.referee_id)

