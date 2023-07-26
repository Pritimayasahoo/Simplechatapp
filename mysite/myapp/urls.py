from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('createaccount/',views.createaccount,name='createaccount'),
    path('login/',views.Loginuser,name='login'),
    path('room/',views.room,name='room'),
    path('createmessage/',views.createmessage,name='createmessage'),
    path('Refresh_message/',views.Refresh_message,name='Refresh_message')

]
