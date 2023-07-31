from django.urls import path

from . import views

urlpatterns = [

    path('login/', view=views.Login, name='login'),
    path('signUp/', view=views.signup, name='signUp'),
    path('verified/', view=views.verify, name='verified'),
   
]
