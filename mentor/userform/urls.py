from django.urls import path
from .views import homePageView
from . import form


urlpatterns = [
    path('', homePageView, name='home'),
    path('createuser/', form.create_user_form, name='createuserform'),
    path('login/', form.login_form, name='loginform')
]
