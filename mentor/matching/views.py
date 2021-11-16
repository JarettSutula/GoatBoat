from django.shortcuts import render

# Create your views here.

def matchPageView(request):
    """View of the match page."""
    return render(request,'match.html')


def mentorFormPageView(request):
    """View of the mentor form page."""
    return render(request,'mentorform.html')


def menteeFormPageView(request):
    """View of the mentee page."""
    return render(request,'menteeform.html')
