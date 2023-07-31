from django.urls import path

from . import views

urlpatterns = [

    # path('login/', view=views.Login, name='login'),
    # path('signUp/', view=views.signup, name='signUp'),
    # path('verified/', view=views.verify, name='verified'),
    path('login/',view=views.login,name='login'),
    path('signUp/',view=views.signUp,name='signUp'),
    path('home/',view=views.home,name='home'),
    path('verify/',view=views.verify,name='verify'),
   
]
