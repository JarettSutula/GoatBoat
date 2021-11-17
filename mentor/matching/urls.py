from django.urls import path
from .views import matchPageView, mentorFormPageView, menteeFormPageView

urlpatterns = [
    path('', matchPageView, name='match'),
    path('mentorform/', mentorFormPageView, name='mentorForm'),
    path('menteeform/', menteeFormPageView, name='menteeform')
]
