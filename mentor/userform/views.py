from django.shortcuts import render
from django.http import HttpResponse

from mentor import userform
import logging

# Create your views here.


def homePageView(request):
    logging.Logger.debug("render home")
    return render(request,'home.html')

def loginView(request):
    logging.Logger.debug("render login header")
    return render(request,'loginheader.html')

def userSucess(request):
    submitbutton= request.POST.get("submit")

    firstname=''
    lastname=''
    emailvalue=''

    form= userform(request.POST or None)
    if form.is_valid():
        firstname= form.cleaned_data.get("first_name")
        lastname= form.cleaned_data.get("last_name")
        emailvalue= form.cleaned_data.get("email")
        logging.Logger.info("form is valid")


    context= {'form': form, 'firstname': firstname, 'lastname':lastname,
              'submitbutton': submitbutton, 'emailvalue':emailvalue}

    logging.Logger.debug("requesting form")
    return render(request, 'form.html', context)

