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

class mentorForm(forms.Form):
    """Contains fields for Mentor Form."""
    username = forms.CharField(max_length=100, label='User Name')
    password = forms.CharField(widget=forms.PasswordInput)
    mentorclasschoice= forms.CharField(label='What class are you looking for help in?', widget=forms.Select(choices=CLASS_CHOICES))

class menteeForm(forms.Form):
    """Contains fields for Mentee Form."""
    username = forms.CharField(max_length=100, label='User Name')
    password = forms.CharField(widget=forms.PasswordInput)
    menteeclasschoice= forms.CharField(label='What class are you looking to  help in?', widget=forms.Select(choices=CLASS_CHOICES))

