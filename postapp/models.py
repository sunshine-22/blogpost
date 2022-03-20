from django.db import models
import datetime


class Registration(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(primary_key=True)
    dob=models.CharField(max_length=15)
    address=models.CharField(max_length=200)
    profile=models.FileField(upload_to="profilephotos/")
    password=models.CharField(max_length=50)
    is_active=models.BooleanField()
class Post(models.Model):
    owner=models.CharField(max_length=100)
    owneremail=models.EmailField()
    description=models.CharField(max_length=1000)
    images=models.FileField(upload_to="posts/")
    date=models.DateField(default=datetime.date.today)
    likes=models.IntegerField(default=0)
    comments=models.TextField(default="")
