import os, sys

from django.forms.fields import CharField
from django.forms.widgets import PasswordInput
from dns.rdataclass import CH
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from utils import start_db, collection_link

import bcrypt

# Create your models here.
CLASS_CHOICES = [
    ('none', ''),
    ('cmpt120', 'CMPT 120'),
    ('cmpt220', 'CMPT 220'),
    ('cmpt221', 'CMPT 221'),
    ('cmpt230', 'CMPT 230'),
    ('cmpt305', 'CMPT 305'),
    ('cmpt306', 'CMPT 306'),
    ('cmpt307', 'CMPT 307'),
    ('cmpt308', 'CMPT 308'),
    ('cmpt330', 'CMPT 330'),
    ('cmpt422', 'CMPT 422'),
    ('cmpt435', 'CMPT 435'),
    ('math210', 'MATH 210'),
    ('math241', 'MATH 241'),
    ('math242', 'MATH 242'),
    ('math310', 'MATH 310'),
    ('math321', 'MATH 321'),
    ('math331', 'MATH 331'),
    ('math343', 'MATH 343'),
    ('math393', 'MATH 393'),
    ('math394', 'MATH 394'),
    ]

TIME_CHOICES = [
    (-1, '---------'),
    (8, '8:00am'),
    (9, '9:00am'),
    (10, '10:00am'),
    (11, '11:00am'),
    (12, '12:00pm'),
    (13, '1:00pm'),
    (14, '2:00pm'),
    (15, '3:00pm'),
    (16, '4:00pm'),
    (17, '5:00pm'),
    (18, '6:00pm'),
    (19, '7:00pm'),
    (20, '8:00pm'),
    (21, '9:00pm'),
    (22, '10:00pm'),
]


class UserForm(forms.Form):
    """Contains fields for profile creation."""
    username = forms.CharField(max_length=100, label='User Name')
    password = forms.CharField(widget=forms.PasswordInput)
    confirmpassword = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    firstname = forms.CharField(max_length=100, label='First Name')
    lastname = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(required=False, label='Your Email Address')
    profession = forms.CharField(max_length=100, label='Profession')
    major = forms.CharField(max_length=100, label='Major')

    mondaystart= forms.IntegerField(required=False, label= 'Monday Availability', widget=forms.Select(choices=TIME_CHOICES))
    mondayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    tuesdaystart= forms.IntegerField(required=False, label= 'Tuesday Availability', widget=forms.Select(choices=TIME_CHOICES))
    tuesdayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    wednesdaystart= forms.IntegerField(required=False, label= 'Wednesday Availability', widget=forms.Select(choices=TIME_CHOICES))
    wednesdayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    thursdaystart= forms.IntegerField(required=False, label= 'Thursday Availability', widget=forms.Select(choices=TIME_CHOICES))
    thursdayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    fridaystart= forms.IntegerField(required=False, label= 'Friday Availability', widget=forms.Select(choices=TIME_CHOICES))
    fridayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    saturdaystart= forms.IntegerField(required=False, label= 'Saturday Availability', widget=forms.Select(choices=TIME_CHOICES))
    saturdayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    sundaystart= forms.IntegerField(required=False, label= 'Sunday Availability', widget=forms.Select(choices=TIME_CHOICES))
    sundayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))

    def clean_username(self):
        """Validate that usernames are unique."""
        username = self.cleaned_data['username']
        db = start_db()
        users = collection_link(db, 'users')
        
        if users.count_documents({'username': username}, limit = 1) != 0:
            raise ValidationError('This username is already in use.')
        else:
            return username

    def clean_confirmpassword(self):
        """Validate that password and confirmed password match."""
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['confirmpassword']
        if pass1 != pass2:
            raise ValidationError('The passwords must match.')
        return pass2

    def clean_mondayend(self):
        """Validates Monday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['mondaystart']
        end = self.cleaned_data['mondayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end

    def clean_tuesdayend(self):
        """Validates Tuesday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['tuesdaystart']
        end = self.cleaned_data['tuesdayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end
    
    def clean_wednesdayend(self):
        """Validates Wednesday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['wednesdaystart']
        end = self.cleaned_data['wednesdayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end
    
    def clean_thursdayend(self):
        """Validates Thursday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['thursdaystart']
        end = self.cleaned_data['thursdayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end
    
    def clean_fridayend(self):
        """Validates Friday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['fridaystart']
        end = self.cleaned_data['fridayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end

    def clean_saturdayend(self):
        """Validates Saturday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['saturdaystart']
        end = self.cleaned_data['saturdayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end

    def clean_sundayend(self):
        """Validates Sunday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['sundaystart']
        end = self.cleaned_data['sundayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end


class LogInForm(forms.Form):
    """Login form with username and password fields."""
    username = forms.CharField(max_length=100, label='User Name')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        """Validates that the username and password exist in database."""
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        db = start_db()
        logins = collection_link(db, 'logins')
    
        # ensure that username and password are valid in database.
        user = logins.find_one({'username':username})
        # if user is not found, it returns None - invalid username.
        if user == None:
            raise ValidationError('There is no account associated with this username.')
        
        # if there is an account with that username, check the password.
        byte_password = password.encode('UTF-8')
        correct_password = bcrypt.checkpw(byte_password, user['password'])
        
        if correct_password:
            print("it matches.")
        else: 
            raise ValidationError('Incorrect password, please try again.')
        

class ProfileSearch(forms.Form):
    """Profile searching form given a username."""
    username = forms.CharField(max_length=100, label='Username')


class EditProfile(forms.Form):
    """Contains fields for editing profile."""
    firstname = forms.CharField(max_length=100, label='First Name')
    lastname = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(required=False, label='Your Email Address')
    profession = forms.CharField(max_length=100, label='Profession')
    major = forms.CharField(max_length=100, label='Major')

    mondaystart= forms.IntegerField(required=False, label= 'Monday Availability', widget=forms.Select(choices=TIME_CHOICES))
    mondayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    tuesdaystart= forms.IntegerField(required=False, label= 'Tuesday Availability', widget=forms.Select(choices=TIME_CHOICES))
    tuesdayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    wednesdaystart= forms.IntegerField(required=False, label= 'Wednesday Availability', widget=forms.Select(choices=TIME_CHOICES))
    wednesdayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    thursdaystart= forms.IntegerField(required=False, label= 'Thursday Availability', widget=forms.Select(choices=TIME_CHOICES))
    thursdayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    fridaystart= forms.IntegerField(required=False, label= 'Friday Availability', widget=forms.Select(choices=TIME_CHOICES))
    fridayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    saturdaystart= forms.IntegerField(required=False, label= 'Saturday Availability', widget=forms.Select(choices=TIME_CHOICES))
    saturdayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))
    sundaystart= forms.IntegerField(required=False, label= 'Sunday Availability', widget=forms.Select(choices=TIME_CHOICES))
    sundayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))

    def clean_mondayend(self):
        """Validates Monday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['mondaystart']
        end = self.cleaned_data['mondayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end

    def clean_tuesdayend(self):
        """Validates Tuesday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['tuesdaystart']
        end = self.cleaned_data['tuesdayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end
    
    def clean_wednesdayend(self):
        """Validates Wednesday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['wednesdaystart']
        end = self.cleaned_data['wednesdayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end
    
    def clean_thursdayend(self):
        """Validates Thursday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['thursdaystart']
        end = self.cleaned_data['thursdayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end
    
    def clean_fridayend(self):
        """Validates Friday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['fridaystart']
        end = self.cleaned_data['fridayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end

    def clean_saturdayend(self):
        """Validates Saturday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['saturdaystart']
        end = self.cleaned_data['saturdayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end

    def clean_sundayend(self):
        """Validates Sunday time availability before form submission.
        Override clean for end value only to reduce function calls.
        End value is the priority - start value is cleaned before it,
        requires both values to be clean to compare.
        """
        start = self.cleaned_data['sundaystart']
        end = self.cleaned_data['sundayend']

        # conditions - cannot be the same time, nor can starttime come after endtime,
        # nor can only one value be empty.
        if (start == end and start != -1) or (start > end) or (start != end and (start == -1 or end == -1)):
            raise ValidationError('Please select a valid time frame.')
        return end


class ResetPassword(forms.Form):
    """Allows logged-in users to reset their password. Includes 
    original password, original password checker, new password,
    new password checker, and a cleaner that ensures that the
    new password is not the same as the old password.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label= "Username")
    oldpassword = CharField(widget=forms.PasswordInput, label= "Old Password")
    confirmoldpassword = CharField(widget=forms.PasswordInput, label= "Confirm Old Password")
    newpassword = CharField(widget=forms.PasswordInput, label= "New Password")
    confirmnewpassword = CharField(widget=forms.PasswordInput, label= "Confirm New Password")

    def clean_confirmoldpassword(self):
        """Raise errors if the passwords do not match."""
        username = self.cleaned_data['username']
        pass1 = self.cleaned_data['oldpassword']
        pass2 = self.cleaned_data['confirmoldpassword']

        if pass1 != pass2:
            raise ValidationError("Your old password does not match its confirmation.")

        db = start_db()
        logins = collection_link(db, 'logins')
        login_context = logins.find_one({'username':username})
        byte_password = pass1.encode('UTF-8')
        
        # check if user's old password is right.
        if bcrypt.checkpw(byte_password, login_context['password']):
            return pass2
        else:
            raise ValidationError("Incorrect password.")

    def clean_confirmnewpassword(self):
        """Raise errors if the passwords do not match."""
        oldpassword = self.cleaned_data['oldpassword']
        pass1 = self.cleaned_data['newpassword']
        pass2 = self.cleaned_data['confirmnewpassword']

        if pass1 != pass2:
            raise ValidationError("Your new password does not match its confirmation.")
        elif oldpassword == pass1:
            raise ValidationError("Your old and new passwords must be different.")
        else:
            return pass2