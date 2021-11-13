from django.shortcuts import render
from django.http import HttpResponse
from utils import collection_link, start_db
from userform.models import UserForm

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
    form = UserForm()
    # if we are logged in, fill the form with current profile values.
    if 'username' in request.session:
        db = start_db()
        users = collection_link(db, 'users')
        current_profile = users.find_one({'username': request.session['username']})

        profile_context = {
            'username': current_profile['username'],
            'firstname': current_profile['firstname'],
            'lastname': current_profile['lastname'],
            'email': current_profile['email'],
            'profession': current_profile['profession'],
            'major': current_profile['major'],
            'mentorclasschoice': current_profile['mentorclasschoice'],
            'menteeclasschoice': current_profile['menteeclasschoice']
        }

        form = UserForm(initial= profile_context)
    
    return render(request, 'editprofile.html', {'form':form})

