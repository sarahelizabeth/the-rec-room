import uuid

from django.db import models
from django.utils.timesince import timesince

from account.models import User

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def modified_at_formatted(self):
       return timesince(self.created_at)


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, null=True)
    body = models.TextField()
    sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    
    def created_at_formatted(self):
       return timesince(self.created_at)