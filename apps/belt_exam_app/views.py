
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request,"belt_exam_app/index.html")


def register(request):
    result = User.objects.validateRegistration(request.POST)
    if "errors" in result:
        for errors in result['errors']:
            messages.error(request,errors)
            return redirect('/')
    else:
        request.session['user_id'] = result['user_id']
    return redirect('/display')

def join(request, id):
    job=Job.objects.get(id=id)
    me = User.objects.get(id= request.session['user_id'])
    job.joined_by.add(me)
    job.save()
    return redirect('/display')

def login(request):
    result= User.objects.validateLogin(request.POST)
    if 'errors' in result:
        messages.error(request, result)
        return redirect('/')
    else:
        request.session['user_id'] = result['user_id']
        return redirect('/display')

def displaypage(request):

    user= User.objects.get(id=request.session['user_id'])
    context={
        'user' :user,
        'all_jobs': Job.objects.exclude(joined_by=user),
        'my_jobs': Job.objects.filter(joined_by=user),
    }


    return render(request, 'belt_exam_app/display.html',context)

def create(request):
    user= User.objects.get(id=request.session['user_id'])
    context={
        'user' :user ,
        'all_jobs': Job.objects.exclude(joined_by=user),
        'my_jobs': Job.objects.filter(joined_by=user),
    }

    return render(request, 'belt_exam_app/addjob.html',context)

def process(request, user_id):

    errors= Job.objects.validateJob(request.POST,request.session['user_id'])
    print('got result')
    if len(errors)>0:
        for error in errors:
            messages.error(request, error)
        return redirect('/create')
    else:
        return redirect('/display')

def deleteJobs(request,job_id):


    b  = Job.objects.get(id=job_id)
    b.delete()

    return redirect('/display')

def cancel(request, id):
	me = User.objects.get(id = request.session['user_id'])
	job = Job.objects.get(id =id)
	job.joined_by.remove(me)
	job.save()
	return redirect('/display')


def edit(request, id):
    context = {
        'job' : Job.objects.get(id=id)
    }
    return render(request, 'belt_exam_app/edit.html', context)

def update_job(request, job_id):

    errors= Job.objects.validateJobUpdate(request.POST, job_id)

    if len(errors)>0:
        for error in errors:
            messages.error(request, error)
        return redirect('/')

    return redirect('/display')


def view(request, id):
    user = User.objects.get(id=request.session['user_id'])
    context={
        "job": Job.objects.get(id=id),
        "user": user
        }


    return render(request, 'belt_exam_app/view.html',context)


def success(request):
    return render(request,"belt_exam_app/success.html")



def logout(request):
    request.session.clear()

    return redirect('/')
