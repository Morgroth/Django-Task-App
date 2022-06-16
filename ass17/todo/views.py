# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TaskEditForm, UserForm,SigninForm,TasksForm
from django.urls import reverse
from django.views import generic
from .models import User,Task
import datetime
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return HttpResponseRedirect(reverse('todo:success'))
    else:
        form = UserForm()

    return render(request, 'todo/sign_up.html', {'form': form})            

def sign_in(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            user_login=form.get_user
            login(request,user_login)
            data=form.cleaned_data
            email=data['email']
            user=get_object_or_404(User,email=email)
            return HttpResponseRedirect(reverse('todo:dashboard',args=(user.email,)))
    else:
        form = SigninForm()
    return render(request, 'todo/sign_in.html', {'form': form})        

class SuccessView(generic.ListView):
    model=User
    template_name='todo/success.html'

@login_required(login_url='todo:login_page')
def dashboard(request):
    email=request.user.email
    user=User.objects.get(email=email)
    tasks = list(user.task_set.values('task_date'))
    dates=[]
    for date in tasks:
        dates.append(date['task_date'])
    dates.sort()
    return render(request,'todo/dashboard.html',{'user':user,'date':datetime.date.today(),'date_list':dates})

@login_required(login_url='todo:login_page')
def add_task(request, email):
    if request.method=='POST':
        form=TasksForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            user=get_object_or_404(User,email=email)
            instance.user=user
            instance.save()
            return HttpResponseRedirect(reverse('todo:dashboard',args=(email,)))
    else:
        form= TasksForm()
    return render(request,'todo/add_a_task.html',{'form':form})            

@login_required(login_url='todo:login_page')
def edit_task(request,email):
    if request.method=='POST':
        form=TaskEditForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            user=get_object_or_404(User,email=email)
            task=user.task_set.get(pk=request.GET['task_id'])
            today=datetime.date.today()
            if task.task_date.date()==today:
                instance.task_name=task.task_name
                instance.user=user
                task.delete()
                instance.save()
                return HttpResponseRedirect(reverse('todo:dashboard',args=(email,)))
            else:
                return render(request,'todo/success.html')
    elif request.method=='GET':
        user=get_object_or_404(User,email=email)
        instance=(user.task_set.get(pk=request.GET['task_id']))
        form=TaskEditForm(instance=instance)     
    return render(request,'todo/edit_task.html',{'form':form})    

@login_required(login_url='todo:login_page')
def task_date(request,email,date):
    user=User.objects.get(email=email)
    date=datetime.datetime.strptime(date, '%m-%d-%Y')
    list_tasks=user.task_set.filter(task_date=date)
    if list_tasks.exists():
        return render(request,'todo/task_list.html',{'task_list':list_tasks})
    else:
        return render(request,'todo/free_day.html')    

@login_required(login_url='todo:login_page')
def date_handler(request,email):
    user=User.objects.get(email=email)
    date=request.POST['date']
    date = datetime.datetime.strptime(date, '%m/%d/%Y')
    list_tasks=user.task_set.filter(task_date=date)
    return render(request,'todo/task_list.html',{'task_list':list_tasks})

@login_required(login_url='todo:login_page')
def logout_view(request):
    if request.method=='POST':
        logout(request)
        return redirect('todo:success')
