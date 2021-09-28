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

class Complain(models.Model):
    uid=models.ForeignKey(Userf,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    place=models.CharField(max_length=50)
    dis=models.TextField()
    creted_on=models.DateTimeField(auto_now_add=True)
    cpic=models.FileField(upload_to='Complain',blank=True,null=True)
    status=models.CharField(default='OPEN',max_length=50)

    def __str__(self):
        return self.uid.fname+' '+self.uid.lname+' > '+self.title

class RentBuyHouse(models.Model):
    uid=models.ForeignKey(Userf,on_delete=models.CASCADE)
    rbaddress=models.CharField(max_length=100)
    rbprice=models.CharField(max_length=50)
    type1=models.CharField(max_length=50)
    rbpic=models.FileField(upload_to='Rent-Buy House',blank=True,null=True)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uid.fname+"  "+self.uid.lname

class Transaction(models.Model):
    made_by = models.ForeignKey(Userf, related_name='transactions', 
                                on_delete=models.CASCADE)
    month=models.CharField(max_length=50)
    year=models.CharField(max_length=50)

    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)







