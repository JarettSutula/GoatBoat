from django import db, forms
from userform.models import UserForm, LogInForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from utils import start_db, collection_link, create_day_object
import bcrypt
db_handle = start_db()
users = collection_link(db_handle, 'users')
logins = collection_link(db_handle, 'logins')


def create_user_form(request):
    submitted = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # base form fields
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            firstname = form.cleaned_data.get("firstname")
            lastname = form.cleaned_data.get("lastname")
            email = form.cleaned_data.get("email")
            profession = form.cleaned_data.get("profession")
            major = form.cleaned_data.get("major")
            mentorclasschoice = form.cleaned_data.get("mentorclasschoice")
            menteeclasschoice = form.cleaned_data.get("menteeclasschoice")

            # schedule-based form fields
            schedule = []
            mondaystart = form.cleaned_data.get("mondaystart")
            mondayend = form.cleaned_data.get("mondayend")
            monday = create_day_object(mondaystart, mondayend, 'monday')
            schedule.append(monday)
            print(schedule)


            context= { 'username': username,
                       'firstname': firstname,
                       'lastname':lastname,
                       'email':email,
                       'profession':profession,
                       'major':major,
                       'mentorclasschoice':mentorclasschoice,
                       'menteeclasschoice':menteeclasschoice,
                       'schedule':schedule
                      }
            
            # make sure the user's username/password is stored safely in logins.
            # hash it in binary string first!
            byte_password = password.encode('UTF-8')
            hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())

            context_2 = { 'username': username,
                          'password': hashed_password
                        }

            print(context)
            
            users.insert_one(context)

            logins.insert_one(context_2)

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

            # do not need this - we are not posting anything in login_form.
            # context= { 'username': username,
            #            'password': password
            #           }

            # print(context)

            # users.insert_one(context)

            return HttpResponseRedirect('/form/login?submitted=True')
    else:
        form = LogInForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'form.html', {'form': form, 'submitted': submitted})