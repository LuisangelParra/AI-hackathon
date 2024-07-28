from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('newchat', views.newchat, name='newchat'),
    path('<int:userchat_id>/chatbot', views.chatbot, name='chatbot'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
]