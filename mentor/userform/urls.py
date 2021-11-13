from django.urls import path
from .views import homePageView, myProfileView, editProfileView
from . import form


urlpatterns = [
    path('', homePageView, name='home'),
    path('createuser/', form.create_user_form, name='createuserform'),
    path('login/', form.login_form, name='loginform'),
    path('profile/', myProfileView, name='myprofile'),
    path('profile/edit/', editProfileView, name='editprofile'),
    path('search/', form.profile_search, name='profilesearch')
]
