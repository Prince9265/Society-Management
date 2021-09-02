from django.db import models
from django.db.models.fields import EmailField

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    pic=models.FileField(upload_to='profile/',null=True,blank=True)
    
    def __str__(self):
        return self.name
# Create your models here.

class Event(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    etitle=models.CharField(max_length=50)
    edate=models.DateField()
    edis=models.TextField()
    epic=models.FileField(upload_to='Event pic',null=True,blank=True)

    def __str__(self):
        return self.uid.name+" > "+self.etitle
