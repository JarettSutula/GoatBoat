from django import db, forms
from matching.models import mentorForm, menteeForm
from django.shortcuts import render
from utils import start_db, collection_link, create_day_array, get_profile_snapshot


db_handle = start_db()

def mentor_form(request):
    """Provides mentor class form for users looking to get help.
    """
    form = mentorForm()
    if request.method == 'POST':
        form = mentorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = form.cleaned_data.get("username")
            return HttpResponseRedirect('/')

    else:
        form = mentorForm()

    return render(request, 'mentorform.html', {'form': form})


def mentee_form(request):
    """Provides mentee form for users looking to help in a class.
    """
    form = menteeForm()
    if request.method == 'POST':
        form = menteeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = form.cleaned_data.get("username")
            return HttpResponseRedirect('/')

    else:
        form = mentorForm()

    return render(request, 'menteeform.html', {'form': form})

