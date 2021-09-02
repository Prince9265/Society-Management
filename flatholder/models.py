from django.db import models
from django.db.models.fields import EmailField

# Create your models here.
class Userf(models.Model):
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=100)
    address = models.TextField()
    password = models.CharField(max_length=100)
    birth = models.DateField()
    occupation = models.CharField(max_length=100,default='')
    pic = models.FileField(upload_to='holderpic/',blank=True,null=True)
    role = models.CharField(default='user',max_length=50)


    def __str__(self):
        return self.fname + '  ' + self.lname
