from django.forms import ModelForm, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from .models import Task, User
from datetime import datetime,timezone
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
  "Sign - up form"                         
  class Meta:
    model=User
    fields=['first_name','last_name','email','std_code','phone_number','gender',]



  # def clean(self):
  #   checked_data=self.cleaned_data
  #   p1=checked_data['password']
  #   p2=checked_data.get('confirm_password')
  #   email_user=checked_data.get('email')
  #   e=User.objects.filter(email=email_user).count()
  #   if e>=1:
  #        raise ValidationError('You are already registered')
  #   if len(p1)<1:
  #     raise ValidationError('Password should be atleast 8 characters long')
  #   if p1!=p2:
  #     raise ValidationError('Passwords don\'t match')      

  #   return checked_data



class SigninForm(ModelForm):
  "Sign - up form"                         
  class Meta:
    model=User
    fields=['email','password']

  def clean(self):
    checked_data=self.cleaned_data
    try:
      user=User.objects.get(email=checked_data['email'])
    except ObjectDoesNotExist:
      raise ValidationError('Email not registered. ')
    if checked_data['password']==user.password:
      return checked_data
    else:
        raise ValidationError('Invalid Password') 

  def get_user(self):
    user=User.objects.get(email=self.cleaned_data['email'])
    try:
      return user
    except User.DoesNotExist:
      return None  

class TasksForm(ModelForm):
  "Contains task making stuff "
  class Meta:
    model = Task
    fields=['task_name','chore','completed','task_date',]
    
  def clean(self):
    checked_data=self.cleaned_data
    try:
     date=checked_data['task_date']
    except KeyError:
      raise ValidationError('Date format is MM/DD/YYYY')
    today=datetime.now(timezone.utc)
    if date.date()<today.date():
      raise ValidationError('You can\'t set tasks for the past' )
    return checked_data  

class TaskEditForm(ModelForm):
  " Contains task editing stuff "
  class Meta:
    model=Task
    fields=['chore','completed','task_date']

  def clean(self):
    checked_data=self.cleaned_data
    date=checked_data['task_date']
    today=datetime.now(timezone.utc).date()
    if date.date()<today:
      raise ValidationError('You can\'t set tasks for the past' )
    return checked_data  

