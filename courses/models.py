from django.db import models
from g4growth.storage_backends import MediaStorage
# Create your models here.
status_choices = (('active', 'ACTIVE'), ('inactive', 'INACTIVE'),('deleted', 'DELETED'))

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    date_added =  models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    title = models.CharField(max_length=50)
    description = models.TextField()
    cover_img = models.FileField(storage= MediaStorage, blank=True, null=True)
    file = models.FileField(storage= MediaStorage, blank=True, null=True)
    status = models.CharField(max_length=8, choices=status_choices, default='active')

    def __str__(self):
        return self.title
