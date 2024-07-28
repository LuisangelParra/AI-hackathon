from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('newchat', views.newchat, name='newchat'),
    path('<int:userchat_id>/chatbot', views.chatbot, name='chatbot'),
    path('<int:userchat_id>/chatbot-delete', views.chatbot_delete, name='chatbot-delete'),
    path('<int:url_id>/chatbot-edit', views.chatbot_edit, name='chatbot-edit'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
]