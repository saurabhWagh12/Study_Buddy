from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10,null=True,blank=True,unique=True)
    
    def __str__(self) -> str:
        return self.user.username
    

class Request(models.Model):
    fromUser = models.EmailField(null=False,blank=False)
    toUser = models.EmailField(null=False,blank=False)
    class Meta:
        unique_together = ('fromUser', 'toUser')

class Buddy(models.Model):
    user1 = models.EmailField(null=False,blank=False)
    user2 = models.EmailField(null=False,blank=False)
    class Meta:
        unique_together = ('user1', 'user2')



