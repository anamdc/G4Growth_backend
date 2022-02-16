from datetime import date
from django.db import models

# Create your models here.

class Credit(models.Model):
    userid = models.IntegerField()
    date = models.DateField(default=date.today)
    amount = models.IntegerField()
    referee = models.IntegerField()

    def __str__(self):
        return str(self.userid)

