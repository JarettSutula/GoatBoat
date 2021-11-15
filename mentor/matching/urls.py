from django.urls import path
from .views import matchPageView


urlpatterns = [
    path('', matchPageView, name='match'),
]
