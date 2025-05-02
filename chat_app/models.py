from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Conversation(models.Model):
    initiator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="convo_starter"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="convo_participant"
    )
    start_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'

    def __str__(self):
        return f"Conversation between {self.initiator} and {self.receiver}."

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, related_name='message_sender')
    text = models.CharField(max_length=200, blank=True)
    attachment = models.FileField(blank=True)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)
        db_table = 'messages'

    def __str__(self):
        return f"sent by {self.sender}."