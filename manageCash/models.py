from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    usertype = [('Depositor','Depositor'),('Creditor','Creditor'),('Treasury','Treasury')]
    user_type = models.CharField(choices=usertype,max_length=20,null=True)
    full_name = models.CharField(max_length=100,null=True)

class AddCashModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.SET_NULL,null =True)
    source = models.CharField(max_length=200,null=True)
    datetime = models.DateField(auto_now_add=True,null=True)
    amount = models.PositiveIntegerField(null=True)
    description = models.TextField()

class ExpenseModel(models.Model):
    user = models.ForeignKey(UserModel,on_delete=models.SET_NULL,null =True)
    description = models.TextField()
    amount = models.PositiveIntegerField(null=True)
    datetime = models.DateField(auto_now_add=True,null=True)