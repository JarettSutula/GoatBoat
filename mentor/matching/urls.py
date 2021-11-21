from django.urls import path
from .views import matchPageView, ClassChoiceFormPageView

urlpatterns = [
    path('', matchPageView, name='match'),
    path('chooseclass/', ClassChoiceFormPageView, name='classChoiceForm'),
]
