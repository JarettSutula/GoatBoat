from django.db import models
from django import forms
from utils import start_db, collection_link, dynamic_class_dropdown
from django.core.exceptions import ValidationError
import bcrypt

# Create your models here.
CLASS_CHOICES = [
    ('none', ''),
    ('CMPT120', 'CMPT 120'),
    ('CMPT220', 'CMPT 220'),
    ('CMPT221', 'CMPT 221'),
    ('CMPT230', 'CMPT 230'),
    ('CMPT305', 'CMPT 305'),
    ('CMPT306', 'CMPT 306'),
    ('CMPT307', 'CMPT 307'),
    ('CMPT308', 'CMPT 308'),
    ('CMPT330', 'CMPT 330'),
    ('CMPT422', 'CMPT 422'),
    ('CMPT435', 'CMPT 435'),
    ('MATH210', 'MATH 210'),
    ('MATH241', 'MATH 241'),
    ('MATH242', 'MATH 242'),
    ('MATH310', 'MATH 310'),
    ('MATH321', 'MATH 321'),
    ('MATH331', 'MATH 331'),
    ('MATH343', 'MATH 343'),
    ('MATH393', 'MATH 393'),
    ('MATH394', 'MATH 394'),
]

ACTION_CHOICES = [
    ('adding', 'adding'),
    ('removing', 'removing'),
]

MENTOR_MENTEE_CHOICES = [
    ('mentee', 'receive'),
    ('mentor', 'give'),
]

class ClassChoiceForm(forms.Form):
    """Contains fields for class choice Form."""
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label= "Username")
    password = forms.CharField(widget=forms.PasswordInput)
    action = forms.CharField(label='Are you adding or removing a class?', widget=forms.Select(choices=ACTION_CHOICES))
    mentormenteechoice = forms.CharField(label='Are you looking to receive help or give help for this class?', widget=forms.Select(choices=MENTOR_MENTEE_CHOICES))
    classchoice= forms.CharField(label='What class are you looking for?', widget=forms.Select(choices=CLASS_CHOICES))

    def clean_password(self):
        """Raise error if the password is incorrect."""
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        db = start_db()
        logins = collection_link(db, 'logins')

        user = logins.find_one({'username': username})
        byte_password = password.encode('UTF-8')

        if bcrypt.checkpw(byte_password, user['password']):
            return password
        else:
            raise ValidationError("Incorrect username or password.")

    def clean_classchoice(self):
        """Raise error if the class they select to post is already
        in their user object.
        """
        username = self.cleaned_data['username']
        classchoice = self.cleaned_data['classchoice']

        if classchoice == 'none':
            raise ValidationError("A class is required.")

        db = start_db()
        users = collection_link(db, 'users')

        user = users.find_one({'username': username})

        action = self.cleaned_data['action']
        mentormentee = self.cleaned_data['mentormenteechoice']
        alreadyexists = "This class already exists on this profile."
        doesntexist = "This class doesn't exist on this profile and can't be removed."

        # If we are adding, ensure class doesn't already exist in the right place.
        if action == 'adding':
            if mentormentee == 'mentor':
                if classchoice in user['mentorclasschoice']:
                    raise ValidationError(alreadyexists)

            elif mentormentee == 'mentee':
                if classchoice in user['menteeclasschoice']:
                    raise ValidationError(alreadyexists)
        
        # if we are removing, ensure class does already exist in the right place.
        elif action == 'removing':
            if mentormentee == 'mentor':
                if classchoice not in user['mentorclasschoice']:
                    raise ValidationError(doesntexist)

            elif mentormentee == "mentee":
                if classchoice not in user['menteeclasschoice']:
                    raise ValidationError(doesntexist)

        # if no errors are raised, just pass back the field as cleaned.
        return classchoice


class MentorMatchForm(forms.Form):
    """Contains fields for matching with a mentor."""
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label= "Username")
    password = forms.CharField(widget=forms.PasswordInput)
    classchoice = forms.CharField()

    # allow username/class choices be passed in through kwargs.
    def __init__(self, *args, **kwargs):
        # pass in a dictionary for user_details.
        user_details = kwargs.pop('user_details', None)
        super(MentorMatchForm, self).__init__(*args, **kwargs)
        # if there is something in it...
        if user_details:
            # set the username (which is hidden) to the logged-in user.
            self.fields['username'].initial = user_details['username']

            # ensure that we have the classes they are looking for by seeing if
            # the menteeclasschoice field is empty - if true, it's not empty.
            if user_details['menteeclasschoice']:
                myclasses = dynamic_class_dropdown(user_details['username'], 'mentee')
                print(myclasses)
                self.fields['classchoice'] = forms.CharField(widget=forms.Select(choices=myclasses))

    def clean_password(self):
        """Raise error if the password is incorrect."""
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        db = start_db()
        logins = collection_link(db, 'logins')

        user = logins.find_one({'username': username})
        byte_password = password.encode('UTF-8')

        if bcrypt.checkpw(byte_password, user['password']):
            return password
        else:
            raise ValidationError("Incorrect password.")


class MenteeMatchForm(forms.Form):
    """Contains fields for matching with a mentee."""
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label= "Username")
    password = forms.CharField(widget=forms.PasswordInput)
    classchoice = forms.CharField()

    # allow username/class choices be passed in through kwargs.
    def __init__(self, *args, **kwargs):
        # pass in a dictionary for user_details.
        user_details = kwargs.pop('user_details', None)
        super(MenteeMatchForm, self).__init__(*args, **kwargs)
        # if there is something in it...
        if user_details:
            # set the username (which is hidden) to the logged-in user.
            self.fields['username'].initial = user_details['username']

            # ensure that we have the classes they are looking for by seeing if
            # the mentorclasschoice field is empty - if true, it's not empty.
            if user_details['mentorclasschoice']:
                myclasses = dynamic_class_dropdown(user_details['username'], 'mentor')
                print(myclasses)
                self.fields['classchoice'] = forms.CharField(widget=forms.Select(choices=myclasses))

    def clean_password(self):
        """Raise error if the password is incorrect."""
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        db = start_db()
        logins = collection_link(db, 'logins')

        user = logins.find_one({'username': username})
        byte_password = password.encode('UTF-8')

        if bcrypt.checkpw(byte_password, user['password']):
            return password
        else:
            raise ValidationError("Incorrect password.")


class MentorSubmissionForm(forms.Form):
    """Contains fields for mentor's username to be used when selecting a match."""
    mentorusername = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label='Mentor Username')


class MenteeSubmissionForm(forms.Form):
    """Contains fields for mentee's username to be used when selecting a match."""
    menteeusername = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label='Mentee Username')
