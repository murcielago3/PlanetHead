

from __future__ import unicode_literals
from django.db import models
import bcrypt
import re


EMAIL_REGEX=  re.compile(r"[^@]+@[^@]+\.[^@]+")

class UserManager(models.Manager):
    def validateRegistration(self, postData):
        result = {}
        errors = []
        if len(postData['first_name']) < 3:
            errors.append('First Name is to short')
        if len(postData['last_name'])<3:
            errors.append(' Last Name is to short')
        if len(postData['email'])<1:
            errors.append(' Email is to short')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append(' Please enter a valid Email')

        if postData['pw'] != postData['cpw']:
            errors.append('Passwords are not matching')
        if len(postData["pw"]) <10 :
            errors.append('Password is to short')
        if len(User.objects.filter(email=postData['email']))>0:
            errors.append('This Email already exist')


        if len(errors) >0:
            result['errors']= errors
            return result
        else:
            me=User.objects.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt())
            ).id
            result['user_id']=me
            return result

    def validateLogin(self,postData):
        result={}
        errors=[]
        existing_user_list= User.objects.filter(email=postData['email'])
        if len(existing_user_list) >0:
            if bcrypt.checkpw(postData['pw'].encode(), existing_user_list[0].password.encode()):
                result['user_id'] = existing_user_list[0].id
            else:
                errors.append('invalid email/password combination')

        else: errors.append('invalid email/password combination')
        if len(errors)>0:
            result['errors']=errors
        return result




    def validateUpdate(self, postData, user_id):
        me = User.objects.get(id=user_id)
        errors = []
        if len(postData['first_name']) == 0:
            errors.append('fill out the first name dimwit')
        if len(postData['last_name']) == 0:
            errors.append('put your last name retard')
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('please enter a real email')
        if len(errors) == 0:
            me.first_name = postData['first_name']
            me.last_name = postData['last_name']
            me.email = postData['email']
            me.save()

        return errors

class User(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add = True)
    updated_at= models.DateTimeField(auto_now = True)
    objects = UserManager()

class JobManager(models.Manager):
    def validateJob(self, postData, user_id):
        print("************ THIS IS JOB MANAGER***********")
        errors=[]
        user= User.objects.get(id= user_id)

        if len(postData['title']) <3:
             errors.append('please enter real title')
        if len(postData['description']) <10:
            errors.append('please enter more information')
        if len(postData['location']) <3:
            errors.append('please enter a valid location')
        if len(errors)==0:
            Job.objects.create(
            title= postData['title'],
            description= postData['description'],
            location= postData['location'],
            uploaded_by=User.objects.get(id=user_id),
            ).joined_by.add(user)
        return errors

    def validateJobUpdate(self, postData, job_id):
        job = Job.objects.get(id=job_id)
        errors = []
        if len(postData['title']) == 0:
            errors.append('please enter a title')
        if len(postData['description']) == 0:
            errors.append('please give us a description')
        if len(postData['location'])==0:
            errrors.append('please enter a real location')
        if len(errors) == 0:
            job.title = postData['title']
            job.description = postData['description']
            job.location= postData['location']
            job.save()

        return errors








class Job(models.Model):
    title= models.CharField(max_length=255)
    description= models.CharField(max_length=255)
    location= models.CharField(max_length=255)
    
    created_at=models.DateTimeField(auto_now_add= True)
    updated_at=models.DateTimeField(auto_now=True)
    uploaded_by=models.ForeignKey(User, related_name='uploaded_jobs')
    joined_by= models.ManyToManyField(User, related_name='joined_jobs')
    objects=JobManager()

    def __repr__(self):
        return f'{self.title}'

    def __str__(self):
        return f'{self.title}'
