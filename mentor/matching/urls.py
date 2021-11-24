from django.urls import path
from .views import matchPageView, ClassChoiceFormPageView, MentorFormPageView

urlpatterns = [
    path('', matchPageView, name='match'),
    path('mentorform/', MentorFormPageView, name='mentorMatch'),
    path('chooseclass/', ClassChoiceFormPageView, name='classChoiceForm'),
]
