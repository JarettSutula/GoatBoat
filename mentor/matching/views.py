from django.shortcuts import render

# Create your views here.

def matchPageView(request):
    """View of the match page."""
    return render(request,'match.html')
