import re
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from matching.models import mentorForm, menteeForm
from utils import start_db, collection_link

db_handle = start_db()
users = collection_link(db_handle, 'users')
logins = collection_link(db_handle, 'logins')

# Create your views here.
def matchPageView(request):
    """View of the match page."""
    return render(request,'match.html')


def mentorFormPageView(request):
    """View of the mentor form page."""
    submitted = False
    form = mentorForm()
    # if we are signed in and posting
    if 'username' in request.session and request.method == 'POST':
        form = mentorForm(request.POST)
        if form.is_valid():
            # update the object's class choices.
            classchoice = form.cleaned_data.get("mentorclasschoice")

            db = start_db()
            users = collection_link(db, 'users')

            # grab the user's mentorclasschoice list.
            user = users.find_one({'username': request.session['username']})
            mentorclasses = user['mentorclasschoice']

            # append the class chosen in the form.
            mentorclasses.append(classchoice)

            # update the user object.
            users.update_one({'username': request.session['username']},
                                {'$set': {'mentorclasschoice': mentorclasses}})
            submitted = True

    # if we are signed in but not posting, fill hidden form with username.
    elif 'username' in request.session:
        form = mentorForm(initial= {'username': request.session['username']})

    else: 
        form = mentorForm()

    return render(request,'mentorform.html', {'form': form, 'submitted': submitted})


def menteeFormPageView(request):
    """View of the mentee page."""
    submitted = False
    form = menteeForm()
    if request.method == 'POST':
        form = menteeForm(request.POST)
        if form.is_valid():
            # do my stuff
            submitted = True

    else: 
        form = menteeForm()

    return render(request,'menteeform.html', {'form': form, 'submitted': submitted})
