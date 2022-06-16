from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,primary_key=True)
    std_code=models.IntegerField(null=True)
    phone_number=models.IntegerField(null=True)
    GENDER_CHOICES=[('M','Male'),('F','Female'),('O','Other')]
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES)
    USERNAME_FIELD='email'    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email

class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    #COMPLETED_CHOICES=[('Y','Yes'),('N','No')]
    completed=models.CharField(max_length=10)
    #completed=models.CharField(max_length=1,choices=COMPLETED_CHOICES)
    task_date=models.DateTimeField()
    task_name=models.CharField(max_length=50)
    chore=models.TextField()
    def __str__(self):
        return self.task_name
