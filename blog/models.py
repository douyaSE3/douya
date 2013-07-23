#coding=utf8

from django.db import models
from django.contrib.auth.models import User
from place.models import Place

class Article(models.Model):
    place = models.ForeignKey(Place)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=14)
    content = models.TextField()
    update_time = models.DateTimeField()
    public = models.BooleanField()

class Comment(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    update_time = models.DateTimeField()
    parent = models.ForeignKey('self',blank=True,null=True)
    article = models.ForeignKey(Article,blank=True,null=True)
