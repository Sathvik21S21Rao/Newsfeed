from django.urls import path
from . import views
urlpatterns=[ path('',views.response,name='response'),path("sign_up",views.sign_up,name="sign_up")]