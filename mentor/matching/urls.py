from django.urls import path
from .views import MenteeMatchingPageView, matchPageView, ClassChoiceFormPageView, MentorFormPageView, MentorMatchingPageView, MenteeFormPageView

urlpatterns = [
    path('', matchPageView, name='match'),
    path('mentorform/', MentorFormPageView, name='mentorMatch'),
    path('chooseclass/', ClassChoiceFormPageView, name='classChoiceForm'),
    path('menteeform/', MenteeFormPageView, name="menteeMatch"),
    path('mentorresults/', MentorMatchingPageView, name="mentorResults" ),
    path('menteeresults/', MenteeMatchingPageView, name='menteeResults')
]
