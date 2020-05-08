from django.db import models
from django.contrib import admin
# Create your models here.


class Users(models.Model):

    username=models.CharField(max_length=250)
    emailid=models.CharField(max_length=250)
    password=models.CharField(max_length=250)


class GeneralLost(models.Model):
    displayflag = models.BooleanField(default=True)
    postid = models.CharField(max_length=250,blank=False,default=None)
    username=models.CharField(max_length=250)
    itemtype=models.CharField(max_length=250)
    description=models.CharField(max_length=250)
    imagelink = models.CharField(max_length=500)
    campuslocation = models.CharField(max_length=250)
    address = models.CharField(max_length=250, default='')
    timestamp = models.DateField('Time Stamp', default=None, blank=True, null=True)

class GeneralFound(models.Model):
    displayflag = models.BooleanField(default=True)
    postid = models.CharField(max_length=250,blank=False,default=None)
    username=models.CharField(max_length=250)
    itemtype=models.CharField(max_length=250)
    description=models.CharField(max_length=250)
    imagelink = models.CharField(max_length=500)
    campuslocation = models.CharField(max_length=250)
    address = models.CharField(max_length=250, default='')
    timestamp = models.DateField('Time Stamp', default=None, blank=True, null=True)

class SensitiveFound(models.Model):
    displayflag = models.BooleanField(default=True)
    postid = models.CharField(max_length=250,blank=False,default=None)
    username=models.CharField(max_length=250,default='')
    cardtype=models.CharField(max_length=250,default='')
    description=models.CharField(max_length=250,default='')
    campuslocation = models.CharField(max_length=250,default='')
    address = models.CharField(max_length=250,default='')
    fourdigit = models.IntegerField(default=0000)
    color = models.CharField(max_length=250,default='')
    timestamp=models.DateField('Time Stamp',default=None, blank=True, null=True)

class SensitiveLost(models.Model):
    displayflag = models.BooleanField(default=True)
    postid = models.CharField(max_length=250,blank=False,default=None)
    username = models.CharField(max_length=250, default='')
    cardtype = models.CharField(max_length=250, default='')
    description = models.CharField(max_length=250, default='')
    campuslocation = models.CharField(max_length=250, default='')
    address = models.CharField(max_length=250, default='')
    fourdigit = models.IntegerField(default=0000)
    color = models.CharField(max_length=250, default='')
    timestamp = models.DateField('Time Stamp', default=None, blank=True, null=True)

