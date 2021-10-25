from django import forms
from userform.models import UserForm, LogInForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from utils import start_db, collection_link
db_handle = start_db()
users = collection_link(db_handle, 'users')


def create_user_form(request):
    submitted = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = form.cleaned_data.get("username")
            firstname = form.cleaned_data.get("firstname")
            lastname = form.cleaned_data.get("lastname")
            email = form.cleaned_data.get("email")
            profession = form.cleaned_data.get("profession")
            major = form.cleaned_data.get("major")
            mentorclasschoice = form.cleaned_data.get("mentorclasschoice")
            menteeclasschoice = form.cleaned_data.get("menteeclasschoice")

            context= { 'username': username,
                       'firstname': firstname,
                       'lastname':lastname,
                       'email':email,
                       'profession':profession,
                       'major':major,
                       'mentorclasschoice':mentorclasschoice,
                       'menteeclasschoice':menteeclasschoice
                      }

            print(context)
            
            users.insert_one(context)

            return HttpResponseRedirect('/form/createuser?submitted=True')
    else:
        form = UserForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'form.html', {'form': form, 'submitted': submitted})


def login_form(request):
    submitted = False
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            context= { 'username': username,
                       'password': password
                      }

            print(context)

            users.insert_one(context)

            return HttpResponseRedirect('/form/login?submitted=True')
    else:
        form = LogInForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'form.html', {'form': form, 'submitted': submitted})