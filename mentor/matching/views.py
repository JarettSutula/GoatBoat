import re
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from matching.models import ClassChoiceForm, MentorMatchForm, MentorSubmissionForm
from utils import find_matching_schedule, get_profile_snapshot
from utils import start_db, collection_link

db_handle = start_db()
users = collection_link(db_handle, 'users')
logins = collection_link(db_handle, 'logins')

# Create your views here.
def matchPageView(request):
    """View of the match page."""
    return render(request,'match.html')

def MentorFormPageView(request):
    """View of the mentor form page."""
    submitted = False
    form = MentorMatchForm()
    user = {}
    # if we are signed in and posting
    if 'username' in request.session and request.method == 'POST':
        form = MentorMatchForm(request.POST)
        db = start_db()
        users = collection_link(db, 'users')
        user = users.find_one({'username': request.session['username']})

        if form.is_valid():
            classchoice = form.cleaned_data.get("classchoice")
            print(classchoice)

            # if valid, move them to matching results with new classchoice in session.
            submitted = True
            request.session['classchoice'] = classchoice

            return render(request,'mentorform.html', {'form': form, 'submitted': submitted, 'user':user})

    # if we are signed in but not posting, fill hidden form with username.
    elif 'username' in request.session:
        # if they are logged in and not posting yet, fill the form with values.
        # need username and respective class choices for dynamic dropdown.
        db = start_db()
        users = collection_link(db, 'users')
        user = users.find_one({'username': request.session['username']})
        user_details = {'username': user['username'],
                        'menteeclasschoice': user['menteeclasschoice']
                        }
        # put the form's username and drop-down choices in.
        form = MentorMatchForm(user_details = user_details)

    else:
        form = MentorMatchForm()

    return render(request,'mentorform.html', {'form': form, 'submitted': submitted, 'user':user})

def ClassChoiceFormPageView(request):
    """View of the mentor form page."""
    submitted = False
    form = ClassChoiceForm()
    user = {}
    # if we are signed in and posting
    if 'username' in request.session and request.method == 'POST':
        form = ClassChoiceForm(request.POST)
        db = start_db()
        users = collection_link(db, 'users')
        user = users.find_one({'username': request.session['username']})

        if form.is_valid():
            # update the object's class choices.
            classchoice = form.cleaned_data.get("classchoice")
            action = form.cleaned_data.get("action")
            mentormentee = form.cleaned_data.get("mentormenteechoice")

            # grab the user's mentorclasschoice list.
            mentorclasses = user['mentorclasschoice']
            menteeclasses = user['menteeclasschoice']

            # append the class chosen in the form.
            if action == "adding":
                if mentormentee == "mentor":
                    mentorclasses.append(classchoice)
                elif mentormentee == "mentee":
                    menteeclasses.append(classchoice)

            elif action == "removing":
                if mentormentee == "mentor":
                    mentorclasses.remove(classchoice)
                elif mentormentee == "mentee":
                    menteeclasses.remove(classchoice)

            # update the user object field, according to mentormentee choice.
            if mentormentee == "mentor":
                users.update_one({'username': request.session['username']},
                                    {'$set': {'mentorclasschoice': mentorclasses}})
            elif mentormentee == "mentee":
                users.update_one({'username': request.session['username']},
                                    {'$set': {'menteeclasschoice': menteeclasses}})

            submitted = True

    # if we are signed in but not posting, fill hidden form with username.
    elif 'username' in request.session:
        # if they are logged in, get 'user' to display their class data.
        db = start_db()
        users = collection_link(db, 'users')
        user = users.find_one({'username': request.session['username']})

        form = ClassChoiceForm(initial= {'username': request.session['username']})

    else: 
        form = ClassChoiceForm()

    return render(request,'classchoiceform.html', {'form': form, 'submitted': submitted, 'user':user})

def MentorMatchingPageView(request):
   """View of the mentor matching page."""
   # grab the class choice from the previous from in session.
   print(request.session['classchoice'])

   form = MentorSubmissionForm()

   submitted = False
   matches_exist = False

   # connect to the DB and grab anyone that has the same class in their mentor class choices.
   db = start_db()
   users = collection_link(db, 'users')
   # get the user's schedule and their matches.
   user = users.find_one({'username':request.session['username']})
   mentormatches = users.find({'mentorclasschoice': request.session['classchoice']})
   matches = []

   # if we have found mentors with the class, loop through them and ensure they
   # have a matching 1-hour block in their schedule.
   # only get a max of 3 mentors!
   if mentormatches is not None and len(matches) <= 3:
       for mentor in mentormatches:
           # see if the mentor has a matching schedule block.
           context_schedule = find_matching_schedule(user['schedule'], mentor['schedule'])
           if context_schedule != None:
               matches_exist = True
               context_profile = get_profile_snapshot(mentor['username'], True)
               matches.append({'profile':context_profile, 'block':context_schedule})

   return render(request, 'mentormatch.html', {'matches_exist':matches_exist, 'matches':matches, 'form':form})



