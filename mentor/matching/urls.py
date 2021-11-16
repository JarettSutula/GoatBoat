from django.urls import path
from .views import matchPageView, mentorFormPageView, menteeFormPageView
from . import form

urlpatterns = [
    path('', matchPageView, name='match'),
    path('mentorform/', form.mentor_form, name='mentorForm'),
    path('menteeform/', form.mentee_form, name='menteeform')
]
