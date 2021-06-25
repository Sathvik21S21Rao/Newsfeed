from django.urls import path
from . import views
urlpatterns=[ path('',views.response,name='response'),path('home',views.login,name="home"),path("sign_up",views.sign_up,name="sign_up"),
path("genres",views.genres,name="genres"),path("logout",views.logout,name="logout"),path("changepass",views.changepass,name="changepass"),path("location",views.location,name="location"),path("article",views.articles,name="article"),]