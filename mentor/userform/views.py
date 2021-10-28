from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def homePageView(request):
    return render(request,'home.html')

def userSucess(request):
    submitbutton= request.POST.get("submit")

    firstname=''
    lastname=''
    emailvalue=''

    form= UserForm(request.POST or None)
    if form.is_valid():
        firstname= form.cleaned_data.get("first_name")
        lastname= form.cleaned_data.get("last_name")
        emailvalue= form.cleaned_data.get("email")


    context= {'form': form, 'firstname': firstname, 'lastname':lastname,
              'submitbutton': submitbutton, 'emailvalue':emailvalue}

    return render(request, 'form.html', context)

