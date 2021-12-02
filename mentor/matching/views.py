import re
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from matching.models import ClassChoiceForm, MentorMatchForm, MentorSubmissionForm, MenteeMatchForm, MenteeSubmissionForm
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

def MenteeFormPageView(request):
    """View of the mentee form page."""
    submitted = False
    form = MenteeMatchForm()
    user = {}
    # if we are signed in and posting
    if 'username' in request.session and request.method == 'POST':
        form = MenteeMatchForm(request.POST)
        db = start_db()
        users = collection_link(db, 'users')
        user = users.find_one({'username': request.session['username']})

        if form.is_valid():
            classchoice = form.cleaned_data.get("classchoice")
            print(classchoice)

            # if valid, move them to matching results with new classchoice in session.
            submitted = True
            request.session['classchoice'] = classchoice

            return render(request,'menteeform.html', {'form': form, 'submitted': submitted, 'user':user})

    # if we are signed in but not posting, fill hidden form with username.
    elif 'username' in request.session:
        # if they are logged in and not posting yet, fill the form with values.
        # need username and respective class choices for dynamic dropdown.
        db = start_db()
        users = collection_link(db, 'users')
        user = users.find_one({'username': request.session['username']})
        user_details = {'username': user['username'],
                        'mentorclasschoice': user['mentorclasschoice']
                        }
        # put the form's username and drop-down choices in.
        form = MenteeMatchForm(user_details = user_details)

    else:
        form = MenteeMatchForm()

    return render(request,'menteeform.html', {'form': form, 'submitted': submitted, 'user':user})

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

    submitted = False
    matches_exist = False

    form = MentorSubmissionForm()

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
    if mentormatches is not None:
        for mentor in mentormatches:
            # see if the mentor has a matching schedule block.
            context_schedule = find_matching_schedule(user['schedule'], mentor['schedule'])
            if context_schedule != None:
                context_profile = get_profile_snapshot(mentor['username'], True)

                # check if the mentor exists already in the current matches of the user.
                mentor_already_exists = False
                for match in user['currentmatches']:
                    if 'mentormatch' in match:
                        if match['mentormatch'] == mentor['username']:
                            mentor_already_exists = True

                # if the mentor was not found in the currentmatches, add them to potential matches.
                if not mentor_already_exists and len(matches) < 3:
                    matches.append({'profile':context_profile, 'block':context_schedule})

        if len(matches) != 0:
            matches_exist = True

        if 'username' in request.session and request.method == 'POST':
            #set form to be bound
            form = MentorSubmissionForm(request.POST)

            if form.is_valid():
                # update the user object's current match field.
                mentorusername = form.cleaned_data.get("mentorusername")

                #start db connection and update the users currentmatch field with mentor username.
                db = start_db()
                users = collection_link(db, 'users')
                
                # get USER and MENTOR to compare and update.
                final_user = users.find_one({'username': request.session['username']})
                final_mentor = users.find_one({'username': mentorusername})

                # get the list of the user's matches so we can append to it.
                user_currentmatches = final_user['currentmatches']
                user_match_context = {'classchoice': request.session['classchoice'],
                                      'mentormatch': mentorusername}
                # update USER
                user_currentmatches.append(user_match_context)
                users.update_one({'username': request.session['username']},{'$set': {'currentmatches': user_currentmatches}})

                # do the same for mentor
                mentor_currentmatches = final_mentor['currentmatches']
                mentor_match_context = {'classchoice': request.session['classchoice'],
                                        'menteematch': final_user['username']}
                # update MENTOR
                mentor_currentmatches.append(mentor_match_context)
                users.update_one({'username': mentorusername},{'$set': {'currentmatches': mentor_currentmatches}})

                #Grab the mentee class choice list, remove the classchoice that was selected at the beginning of finding
                #a match, and update the user object.
                menteeclasslist = final_user['menteeclasschoice']
                menteeclasslist.remove(request.session['classchoice'])
                users.update_one({'username': request.session['username']},{'$set': {'menteeclasschoice': menteeclasslist}})

                # # update the mentor's class choices as well
                mentorclasslist = final_mentor['mentorclasschoice']
                mentorclasslist.remove(request.session['classchoice'])
                users.update_one({'username': mentorusername}, {'$set': {'mentorclasschoice': mentorclasslist}} )

                # changing user and mentor's schedule.
                #  relevant_block is the 1-hour block user and mentor matched on
                relevant_block = {}

                # get the appropriate block they matched on based on username
                for mentor in matches:
                    if mentor['profile']['username'] == mentorusername :
                        relevant_block = mentor['block']

                # un-capitalize the block's day.
                day_matched = relevant_block['day']
                day_matched = day_matched.lower()
                relevant_block['day'] = day_matched

                # get the schedule blocks to update and later pass into the database.
                userblock = final_user['schedule']
                mentorblock = final_mentor['schedule']

                # pass in the day they matched on and remove that 1-hour block.
                final_user_day = userblock[relevant_block['day']]
                final_mentor_day = mentorblock[relevant_block['day']]

                # update the user's day block.
                for one_hour_block in final_user_day:
                    if one_hour_block['starttime'] == relevant_block['starttime']:
                        final_user_day.remove(one_hour_block)
                # update the mentor's day block
                for one_hour_block in final_mentor_day:
                    if one_hour_block['starttime'] == relevant_block['starttime']:
                        final_mentor_day.remove(one_hour_block)
                
                # update the entire schedule block
                userblock[relevant_block['day']] = final_user_day
                mentorblock[relevant_block['day']] = final_user_day

                # update the respective database objects with the updated schedule blocks
                users.update_one({'username': request.session['username']},{'$set': {'schedule': userblock}})
                users.update_one({'username': mentorusername},{'$set': {'schedule': mentorblock}})

                submitted = True
            else:
                #printing errors that caused form to be invalid
                print("form not valid")
                print(request.POST)
                print(form.errors)
                print(form.is_bound)
        else:
            #printing errors when form is not a POST
            print("request is not a POST")
            print(request.POST)
            print(form.errors)

    return render(request, 'mentormatch.html', {'form':form, 'matches_exist':matches_exist, 'matches':matches, 'submitted':submitted})


def MenteeMatchingPageView(request):
    """View of the mentee matching page."""
    # grab the class choice from the previous from in session.
    print(request.session['classchoice'])

    submitted = False
    matches_exist = False

    form = MenteeSubmissionForm()

    # connect to the DB and grab anyone that has the same class in their mentee class choices.
    db = start_db()
    users = collection_link(db, 'users')
    # get the user's schedule and their matches.
    user = users.find_one({'username':request.session['username']})
    menteematches = users.find({'menteeclasschoice': request.session['classchoice']})
    matches = []

    # if we have found mentees with the class, loop through them and ensure they
    # have a matching 1-hour block in their schedule.
    # only get a max of 3 mentees!
    if menteematches is not None:
        for mentee in menteematches:
            # see if the mentee has a matching schedule block.
            context_schedule = find_matching_schedule(user['schedule'], mentee['schedule'])
            if context_schedule != None:
                context_profile = get_profile_snapshot(mentee['username'], True)

                # check if the mentee exists already in the current matches of the user.
                mentee_already_exists = False
                for match in user['currentmatches']:
                    if 'menteematch' in match:
                        if match['menteematch'] == mentee['username']:
                            mentee_already_exists = True

                # if the mentor was not found in the currentmatches, add them to potential matches.
                if not mentee_already_exists and len(matches) < 3:
                    matches.append({'profile':context_profile, 'block':context_schedule})

        if len(matches) != 0:
            matches_exist = True

        if 'username' in request.session and request.method == 'POST':
            #set form to be bound
            form = MenteeSubmissionForm(request.POST)

            if form.is_valid():
                # update the user object's current match field.
                menteeusername = form.cleaned_data.get("menteeusername")

                #start db connection and update the users currentmatch field with mentor username.
                db = start_db()
                users = collection_link(db, 'users')
                
                # get USER and MENTEE to compare and update.
                final_user = users.find_one({'username': request.session['username']})
                final_mentee = users.find_one({'username': menteeusername})

                # get the list of the user's matches so we can append to it.
                user_currentmatches = final_user['currentmatches']
                user_match_context = {'classchoice': request.session['classchoice'],
                                      'menteematch': menteeusername}
                # update USER
                user_currentmatches.append(user_match_context)
                users.update_one({'username': request.session['username']},{'$set': {'currentmatches': user_currentmatches}})

                # do the same for mentee
                mentee_currentmatches = final_mentee['currentmatches']
                mentee_match_context = {'classchoice': request.session['classchoice'],
                                        'mentormatch': final_user['username']}
                # update MENTEE
                mentee_currentmatches.append(mentee_match_context)
                users.update_one({'username': menteeusername},{'$set': {'currentmatches': mentee_currentmatches}})

                #Grab the mentor class choice list, remove the classchoice that was selected at the beginning of finding
                #a match, and update the user object.
                mentorclasslist = final_user['mentorclasschoice']
                mentorclasslist.remove(request.session['classchoice'])
                users.update_one({'username': request.session['username']},{'$set': {'mentorclasschoice': mentorclasslist}})

                # # update the mentee's class choices as well
                menteeclasslist = final_mentee['menteeclasschoice']
                menteeclasslist.remove(request.session['classchoice'])
                users.update_one({'username': menteeusername}, {'$set': {'menteeclasschoice': menteeclasslist}} )

                # changing user and mentee's schedule.
                #  relevant_block is the 1-hour block user and mentor matched on
                relevant_block = {}

                # get the appropriate block they matched on based on username
                for mentee in matches:
                    if mentee['profile']['username'] == menteeusername :
                        relevant_block = mentee['block']

                # un-capitalize the block's day.
                day_matched = relevant_block['day']
                day_matched = day_matched.lower()
                relevant_block['day'] = day_matched

                # get the schedule blocks to update and later pass into the database.
                userblock = final_user['schedule']
                menteeblock = final_mentee['schedule']

                # pass in the day they matched on and remove that 1-hour block.
                final_user_day = userblock[relevant_block['day']]
                final_mentee_day = menteeblock[relevant_block['day']]

                # update the user's day block.
                for one_hour_block in final_user_day:
                    if one_hour_block['starttime'] == relevant_block['starttime']:
                        final_user_day.remove(one_hour_block)
                # update the mentee's day block
                for one_hour_block in final_mentee_day:
                    if one_hour_block['starttime'] == relevant_block['starttime']:
                        final_mentee_day.remove(one_hour_block)
                
                # update the entire schedule block
                userblock[relevant_block['day']] = final_user_day
                menteeblock[relevant_block['day']] = final_user_day

                # update the respective database objects with the updated schedule blocks
                users.update_one({'username': request.session['username']},{'$set': {'schedule': userblock}})
                users.update_one({'username': menteeusername},{'$set': {'schedule': menteeblock}})
                submitted = True
            else:
                #printing errors that caused form to be invalid
                print("form not valid")
                print(request.POST)
                print(form.errors)
                print(form.is_bound)
        else:
            #printing errors when form is not a POST
            print("request is not a POST")
            print(request.POST)
            print(form.errors)

    return render(request, 'menteematch.html', {'form':form, 'matches_exist':matches_exist, 'matches':matches, 'submitted':submitted})
