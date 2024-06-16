from django.db import models
import uuid
from AquaAccount.models import User

# Create your models here.

class Message(models.Model):
    """
    This Django model represents a chat message between users.

    :param models.Model: Inherits from Django's Model class.
    :type models.Model: class

    :ivar UUIDField message_id: Unique ID for the message, auto-generated.
    :ivar ForeignKey sender_id: Reference to User who sent the message.
    :ivar ForeignKey recipient_id: Reference to User who is the recipient of the message.
    :ivar TextField body: Body of the message.
    :ivar BooleanField is_read: Field to mark whether the message has been read.
    :ivar DateTimeField send_timestamp: Timestamp when the message was sent.
    :ivar DateTimeField view_timestamp: Timestamp when the message was viewed.
    """
    message_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_id')
    recipient_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient_id')
    body = models.TextField(max_length=5000)
    is_read = models.BooleanField(default=False)
    send_timestamp = models.DateTimeField(auto_now_add=True)
    view_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return str(f"{self.message_id} {self.send_timestamp}: {self.sender_id}: {self.body}")

class Matches(models.Model):
    """
    A class used to represent the Matches model.

    ...

    Attributes:
    id (UUIDField): The UUID of the match
    first_user (User): The first user involved in the match
    second_user (User): The second user involved in the match
    first_status (bool): The status of the first user
    second_status (bool): The status of the second user

    ...

    Methods:
    __str__(): Returns the string representation of the match
    """
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    first_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user')
    first_status = models.BooleanField(null=True, blank=True)
    second_status = models.BooleanField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.first_user) + " + " + str(self.second_user) + " = " + str(self.second_status)
