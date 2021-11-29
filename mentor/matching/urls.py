from django.urls import path
from .views import matchPageView, ClassChoiceFormPageView, MentorFormPageView, MentorMatchingPageView

urlpatterns = [
    path('', matchPageView, name='match'),
    path('mentorform/', MentorFormPageView, name='mentorMatch'),
    path('chooseclass/', ClassChoiceFormPageView, name='classChoiceForm'),
    path('mentormatching/', MentorMatchingPageView, name='mentorMatching'),
]
