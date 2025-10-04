from django.db import models


class Conversation(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        CLOSED = 'CLOSED', 'Closed'

    id = models.CharField(primary_key=True, max_length=100)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id} - {self.status}"


class Message(models.Model):
    class Direction(models.TextChoices):
        SENT = 'SENT', 'Sent'
        RECEIVED = 'RECEIVED', 'Received'

    id = models.CharField(primary_key=True, max_length=100)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    direction = models.CharField(max_length=10, choices=Direction.choices)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from Conversation {self.conversation.id}"
