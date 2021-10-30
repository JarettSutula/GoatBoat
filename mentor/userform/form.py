from django import db, forms
from userform.models import UserForm, LogInForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from utils import start_db, collection_link, create_day_array
import bcrypt
db_handle = start_db()
users = collection_link(db_handle, 'users')
logins = collection_link(db_handle, 'logins')


def create_user_form(request):
    """Validates user creation form and returns appropriate response.
    If the form is valid, insert inputs into database and return HTTPResponseRedirect:
    If not, return the previously filled form values and alert user of validation errors.
    """
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
            mondaystart = form.cleaned_data.get("mondaystart")
            mondayend = form.cleaned_data.get("mondayend")
            tuesdaystart = form.cleaned_data.get("tuesdaystart")
            tuesdayend = form.cleaned_data.get("tuesdayend")
            wednesdaystart = form.cleaned_data.get("wednesdaystart")
            wednesdayend = form.cleaned_data.get("wednesdayend")
            thursdaystart = form.cleaned_data.get("thursdaystart")
            thursdayend = form.cleaned_data.get("thursdayend")
            fridaystart = form.cleaned_data.get("fridaystart")
            fridayend = form.cleaned_data.get("fridayend")
            saturdaystart = form.cleaned_data.get("saturdaystart")
            saturdayend = form.cleaned_data.get("saturdayend")
            sundaystart = form.cleaned_data.get("sundaystart")
            sundayend = form.cleaned_data.get("sundayend")

            # create arrays of objects with 1-hour block objects.
            monday = create_day_array(mondaystart, mondayend)
            tuesday = create_day_array(tuesdaystart, tuesdayend)
            wednesday = create_day_array(wednesdaystart, wednesdayend)
            thursday = create_day_array(thursdaystart, thursdayend)
            friday = create_day_array(fridaystart, fridayend)
            saturday = create_day_array(saturdaystart, saturdayend)
            sunday = create_day_array(sundaystart, sundayend)

            # object to be passed into users
            context= { 'username': username,
                       'firstname': firstname,
                       'lastname':lastname,
                       'email':email,
                       'profession':profession,
                       'major':major,
                       'mentorclasschoice':mentorclasschoice,
                       'menteeclasschoice':menteeclasschoice,
                       'schedule':{
                           'monday': monday,
                           'tuesday': tuesday,
                           'wednesday': wednesday,
                           'thursday': thursday,
                           'friday': friday,
                           'saturday': saturday,
                           'sunday': sunday
                       }
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