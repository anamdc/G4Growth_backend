from ast import Delete
import profile
from urllib import request
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from g4growth.storage_backends import PublicMediaStorage2
# Create your models here.


class User(AbstractBaseUser):
    phoneno = models.BigIntegerField(unique=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    profile_img = models.ImageField(storage = PublicMediaStorage2, blank=True)
    referral_id = models.CharField(max_length=9, unique=True, blank=True)
    referrer_id = models.CharField(max_length=9, blank=True)
    total_credit = models.IntegerField(default=0)
    total_debit = models.IntegerField(default=0)
    email = models.EmailField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.IntegerField(blank=True, null=True)
    ifsc_code = models.CharField(max_length=100, blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    otp_validity = models.DateTimeField(blank=True, null=True)
    is_logged = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'phoneno'

    def __str__(self):
        return str(self.phoneno) + '|' + str(self.name)

