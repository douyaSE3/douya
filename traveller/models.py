#coding=utf8

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    MAN = 0
    WOMAN = 1
    SEX_CHOICES = ((MAN,'男'),(WOMAN,'女'),)

    portrait = models.ImageField(upload_to="portrait/",blank=True,null=True)
    phone = models.CharField(max_length=20,blank=True)
    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES)
    introduction = models.TextField(blank=True)
    user = models.OneToOneField(User,primary_key =True)
