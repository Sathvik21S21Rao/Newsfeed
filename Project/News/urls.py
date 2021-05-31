from django.urls import path
from . import views
urlpatterns=[ path('',views.response,name='response'),path('home',views.login,name="home"),path("sign_up",views.sign_up,name="sign_up"),
path("genres",views.genres,name="genres"),path("home",views.home,name="home"),]