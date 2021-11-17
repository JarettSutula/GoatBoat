from django.db import models
from django import forms
from utils import start_db, collection_link
from django.core.exceptions import ValidationError
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

class mentorForm(forms.Form):
    """Contains fields for Mentor Form."""
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label= "Username")
    password = forms.CharField(widget=forms.PasswordInput)
    mentorclasschoice= forms.CharField(label='What class are you looking for help in?', widget=forms.Select(choices=CLASS_CHOICES))

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

    def clean_mentorclasschoice(self):
        """Raise error if the class they select to post is already
        in their user object.
        """
        username = self.cleaned_data['username']
        classchoice = self.cleaned_data['mentorclasschoice']

        db = start_db()
        users = collection_link(db, 'users')

        user = users.find_one({'username': username})

        # see if the class is already in the user object.
        if classchoice in user['mentorclasschoice']:
            raise ValidationError("You already have this class on your profile.")
        else:
            return classchoice


class menteeForm(forms.Form):
    """Contains fields for Mentee Form."""
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label= "Username")
    password = forms.CharField(widget=forms.PasswordInput)
    menteeclasschoice= forms.CharField(label='What class are you looking to  help in?', widget=forms.Select(choices=CLASS_CHOICES))

