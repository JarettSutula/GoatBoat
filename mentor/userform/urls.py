from django.urls import path
from .views import homePageView
from . import form


urlpatterns = [
    path('', homePageView, name='home'),
    path('form/', form.form, name='form')
]
