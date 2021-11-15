from re import sub
import bcrypt
from django.shortcuts import render
from django.http import HttpResponse
from utils import collection_link, start_db, restructure_day_array, create_day_array
from userform.models import UserForm, EditProfile, ResetPassword

# Create your views here.


def homePageView(request):
    """View of the home page."""
    return render(request,'home.html')

def loginView(request):
    "View for the login page."
    return render(request,'loginheader.html')

def myProfileView(request):
    """View for the user's profile.
    This will return relevant user object fields to the html page.
    """
    # before checking anything, initialize blank context. If they don't log in and 
    # still find themselves on profile, blank context will remove errors.
    context = {}
    # if they are logged in, make the object to pass to html.
    if 'username' in request.session:
        db = start_db()
        users = collection_link(db, 'users')
        result = users.find_one({'username': request.session['username']})
        
        # object for html
        context = {
            'username': result['username'],
            'firstname': result['firstname'],
            'lastname': result['lastname'],
            'email': result['email'],
            'profession': result['profession'],
            'major': result['major'],
            'mentorclasschoice': result['mentorclasschoice'],
            'menteeclasschoice': result['menteeclasschoice']
        }

    return render(request,'myprofile.html', {'context':context})

def userSuccess(request):
    submitbutton= request.POST.get("submit")

    firstname=''
    lastname=''
    emailvalue=''

    form= UserForm(request.POST or None)
    if form.is_valid():
        firstname= form.cleaned_data.get("first_name")
        lastname= form.cleaned_data.get("last_name")
        emailvalue= form.cleaned_data.get("email")


    context= {'form': form, 'firstname': firstname, 'lastname':lastname,
              'submitbutton': submitbutton, 'emailvalue':emailvalue}

    return render(request, 'form.html', context)

def editProfileView(request):
    """Pulls up an editable profile, with previously inputted
    values placed already in the form.
    """
    profile_context = {}
    form = EditProfile()
    submitted = False

    if 'username' in request.session and request.method == 'POST':
        form = EditProfile(request.POST)
        if form.is_valid():
            # Base form fields
            firstname = form.cleaned_data.get("firstname")
            lastname = form.cleaned_data.get("lastname")
            email = form.cleaned_data.get("email")
            profession = form.cleaned_data.get("profession")
            major = form.cleaned_data.get("major")
            mentorclasschoice = form.cleaned_data.get("mentorclasschoice")
            menteeclasschoice = form.cleaned_data.get("menteeclasschoice")

            # Schedule-based form fields
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

            # Create arrays of objects with 1-hour block objects.
            monday = create_day_array(mondaystart, mondayend)
            tuesday = create_day_array(tuesdaystart, tuesdayend)
            wednesday = create_day_array(wednesdaystart, wednesdayend)
            thursday = create_day_array(thursdaystart, thursdayend)
            friday = create_day_array(fridaystart, fridayend)
            saturday = create_day_array(saturdaystart, saturdayend)
            sunday = create_day_array(sundaystart, sundayend)

            # Object to be passed into users
            user_context= { 'username': request.session['username'],
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
            
            # update database object.
            db = start_db()
            users = collection_link(db, 'users')

            # update the user from their username and whatever fields they changed.
            users.update_one({'username': request.session['username']},
                             {'$set': user_context})
                             
            # tell HTML that we are submitted.
            submitted = True

    # if we are logged in, fill the form with current profile values.
    elif 'username' in request.session:
        db = start_db()
        users = collection_link(db, 'users')
        current_profile = users.find_one({'username': request.session['username']})

        # need to translate current schedule to mondaystart, mondayend ... etc
        # without it, form will not display proper schedule.
        mondaystart, mondayend = restructure_day_array(current_profile['schedule']['monday'])
        tuesdaystart, tuesdayend = restructure_day_array(current_profile['schedule']['tuesday'])
        wednesdaystart, wednesdayend = restructure_day_array(current_profile['schedule']['wednesday'])
        thursdaystart, thursdayend = restructure_day_array(current_profile['schedule']['thursday'])
        fridaystart, fridayend = restructure_day_array(current_profile['schedule']['friday'])
        saturdaystart, saturdayend = restructure_day_array(current_profile['schedule']['saturday'])
        sundaystart, sundayend = restructure_day_array(current_profile['schedule']['sunday'])

        # pass the relevant user profile form fields into an object.
        profile_context = {
            'username': current_profile['username'],
            'firstname': current_profile['firstname'],
            'lastname': current_profile['lastname'],
            'email': current_profile['email'],
            'profession': current_profile['profession'],
            'major': current_profile['major'],
            'mentorclasschoice': current_profile['mentorclasschoice'],
            'menteeclasschoice': current_profile['menteeclasschoice'],
            'mondaystart': mondaystart,
            'mondayend': mondayend,
            'tuesdaystart': tuesdaystart,
            'tuesdayend': tuesdayend,
            'wednesdaystart': wednesdaystart,
            'wednesdayend': wednesdayend,
            'thursdaystart': thursdaystart,
            'thursdayend': thursdayend,
            'fridaystart': fridaystart,
            'fridayend': fridayend,
            'saturdaystart': saturdaystart,
            'saturdayend': saturdayend,
            'sundaystart': sundaystart,
            'sundayend': sundayend
        }

        form = EditProfile(initial= profile_context)
    
    else:
        form = EditProfile()
    
    return render(request, 'editprofile.html', {'form':form, 'submitted':submitted})

def changePasswordView(request):
    """Allows user to change their password."""
    form = ResetPassword()
    submitted = False
    
    if 'username' in request.session and request.method == 'POST':
        form = ResetPassword(request.POST)
        if form.is_valid():
            submitted = True
            newpassword = form.cleaned_data.get("newpassword")

            db = start_db()
            logins = collection_link(db, 'logins')
    
            # encode and hash the new password
            new_pass = newpassword.encode('UTF-8')
            new_pass_hashed = bcrypt.hashpw(new_pass, bcrypt.gensalt())

            # pass the new password into the db.
            logins.update_one({'username': request.session['username']},
                                {'$set': {'password':new_pass_hashed}})
            submitted = True

    elif 'username' in request.session:
        # load the form with the current logged-in username.
        form = ResetPassword(initial={'username': request.session['username']})

    else:
        form = ResetPassword()

    return render(request, 'resetpassword.html', {'form':form, 'submitted':submitted})
