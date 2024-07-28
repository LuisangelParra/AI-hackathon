from django.db import models
from django.contrib.auth.models import User

class UserChatList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    userchat_macro = models.ForeignKey(UserChatList, on_delete=models.CASCADE, null=True)

class TrainingData(models.Model):
    prompt = models.TextField()
    response = models.TextField()