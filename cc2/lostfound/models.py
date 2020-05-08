from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.


class Users(models.Model):
    username=models.CharField(max_length=250)
    emailid=models.CharField(max_length=250)
    password=models.CharField(max_length=250)


class GeneralLost(models.Model):

    title=models.CharField(max_length=250,default='')
    displayflag = models.BooleanField(default=True)
    postid = models.CharField(max_length=250,blank=False,default=None)
    user = models.ForeignKey(User, related_name='gl_user',null=True, on_delete=models.SET_NULL)
    itemtype=models.CharField(max_length=250)
    description=models.CharField(max_length=250)
    imagelink = models.CharField(max_length=500)
    campuslocation = models.CharField(max_length=250)
    address = models.CharField(max_length=250, default='')
    timestamp = models.DateField('Time Stamp', default=None, blank=True, null=True)
    lost_found_date = models.CharField(max_length=250,default='')

class GeneralFound(models.Model):

    title=models.CharField(max_length=250,default='')
    displayflag = models.BooleanField(default=True)
    postid = models.CharField(max_length=250,blank=False,default=None)
    user = models.ForeignKey(User, related_name='gf_user',null=True, on_delete=models.SET_NULL)
    itemtype=models.CharField(max_length=250)
    description=models.CharField(max_length=250)
    imagelink = models.CharField(max_length=500)
    campuslocation = models.CharField(max_length=250)
    address = models.CharField(max_length=250, default='')
    timestamp = models.DateField('Time Stamp', default=None, blank=True, null=True)
    lost_found_date = models.CharField(max_length=250,default='')


class SensitiveFound(models.Model):

    title = models.CharField(max_length=250,default='')
    displayflag = models.BooleanField(default=True)
    postid = models.CharField(max_length=250,blank=False,default=None)
    user = models.ForeignKey(User, related_name='sf_user',null=True, on_delete=models.SET_NULL)
    cardtype=models.CharField(max_length=250,default='')
    description=models.CharField(max_length=250,default='')
    campuslocation = models.CharField(max_length=250,default='')
    address = models.CharField(max_length=250,default='')
    fourdigit = models.IntegerField(default=0000)
    color = models.CharField(max_length=250,default='')
    timestamp=models.DateField('Time Stamp',default=None, blank=True, null=True)
    lost_found_date = models.CharField(max_length=250,default='')

class SensitiveLost(models.Model):

    title = models.CharField(max_length=250,default='')
    displayflag = models.BooleanField(default=True)
    postid = models.CharField(max_length=250,blank=False,default=None)
    user = models.ForeignKey(User, related_name='sl_user',null=True, on_delete=models.SET_NULL)
    cardtype = models.CharField(max_length=250, default='')
    description = models.CharField(max_length=250, default='')
    campuslocation = models.CharField(max_length=250, default='')
    address = models.CharField(max_length=250, default='')
    fourdigit = models.IntegerField(default=0000)
    color = models.CharField(max_length=250, default='')
    timestamp = models.DateField('Time Stamp', default=None, blank=True, null=True)
    lost_found_date = models.CharField(max_length=250,default='')
