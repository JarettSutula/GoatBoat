from django.urls import path
from .views import matchPageView, ClassChoiceFormPageView

urlpatterns = [
    path('', matchPageView, name='match'),
    path('match/mentorform', matchPageView, name='match'),
    path('match/menteeform', matchPageView, name='match'),
    path('chooseclass/', ClassChoiceFormPageView, name='classChoiceForm'),
]
