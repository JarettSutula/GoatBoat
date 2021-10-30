from django.core.exceptions import ValidationError
from django.db import models
from django import forms

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
    (-1, '-----'),
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
    username = forms.CharField(max_length=100, label='User Name')
    password = forms.CharField(widget=forms.PasswordInput)
    confirmpassword = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)
    firstname = forms.CharField(max_length=100, label='First Name')
    lastname = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(required=False, label='Your Email Address')
    profession = forms.CharField(max_length=100, label='Profession')
    major = forms.CharField(max_length=100, label='Major')
    mentorclasschoice= forms.CharField(label='What class are you looking to tutor for?', widget=forms.Select(choices=CLASS_CHOICES))
    menteeclasschoice= forms.CharField(label='What class are you looking for help in?', widget=forms.Select(choices=CLASS_CHOICES))
    mondaystart= forms.IntegerField(required=False, label= 'Monday Availability', widget=forms.Select(choices=TIME_CHOICES))
    mondayend= forms.IntegerField(required=False, label= ' to ', widget=forms.Select(choices=TIME_CHOICES))

    def clean_confirmpassword(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['confirmpassword']
        if pass1 != pass2:
            raise ValidationError('The passwords must match.')
        return pass2
        

class LogInForm(forms.Form):
    username = forms.CharField(max_length=100, label='User Name')
    password = forms.CharField(widget=forms.PasswordInput)
