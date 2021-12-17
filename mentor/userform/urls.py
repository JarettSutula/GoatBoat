from django.urls import path
from .views import homePageView, myProfileView, editProfileView, changePasswordView, createUserView, loginFormView, profileSearchView

urlpatterns = [
    path('', homePageView, name='home'),
    path('createuser/', createUserView, name='createuserform'),
    path('login/', loginFormView, name='loginform'),
    path('profile/', myProfileView, name='myprofile'),
    path('profile/edit/', editProfileView, name='editprofile'),
    path('search/', profileSearchView, name='profilesearch'),
    path('changepassword/', changePasswordView, name = 'changepassword')
]
