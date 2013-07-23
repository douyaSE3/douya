#coding=utf8

from django.db import models
from django.contrib.auth.models import User
import datetime

class Place(models.Model): 
    chinese_name = models.TextField()
    english_name = models.TextField()
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self',blank=True,null=True)
    has_img = models.BooleanField(default=False)

    def __unicode__(self):
        return self.chinese_name+'  '+self.english_name

class Relationship(models.Model):
    WANT = 0
    BEEN = 1
    BEING = 2
    STATUS_CHOICES = ((WANT,'想去'),(BEEN,'去过'),(BEING,'在这儿'),)

    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    RANK_CHOICES = ((ONE,'一星'),(TWO,'二星'),(THREE,'三星'),(FOUR,'四星'),(FIVE,'五星'),)

    place = models.ForeignKey(Place)
    user = models.ForeignKey(User)
    date = models.DateField(blank=True,null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    rank = models.PositiveSmallIntegerField(blank=True,null=True,choices=RANK_CHOICES)
    text = models.TextField(blank=True)

class Plan(models.Model):
    title = models.CharField(max_length=14)
    user = models.ForeignKey(User)
    public = models.BooleanField()


class Play(models.Model):
    plan = models.ForeignKey(Plan)
    place = models.ForeignKey(Place)
    begin_time = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)
    tips = models.TextField(blank=True)
    cost = models.FloatField(blank=True,null=True,default=0)
    order = models.IntegerField(blank=True,null=True)

class Route(models.Model):
    FOOT = 0
    BIKE = 1
    CAR = 2
    BUS = 3
    TRAIN = 4
    PLANE = 5
    BOAT = 6
    OTHER =7
    TRANS_CHOICES = ((FOOT,'步行'),(BIKE,'自行车'),(CAR,'驾车'),(BUS,'公交'),(TRAIN,'火车'),(PLANE,'飞机'),(BOAT,'轮船'),(OTHER,'未知'),)

    plan = models.ForeignKey(Plan)
    end_play = models.OneToOneField(Play,related_name="prev")
    begin_time = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)
    transportation = models.PositiveSmallIntegerField(blank=True,null=True,choices=TRANS_CHOICES,default=7)
    tips = models.TextField(blank=True)
    cost = models.FloatField(blank=True,null=True,default=0)

class Photo(models.Model):
    plan = models.ForeignKey(Plan)
    place = models.ForeignKey(Place)
    title = models.CharField(max_length=14)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="photo/")
    upload_time = models.DateTimeField()

