from django.db import models

# Create your models here.
#from django.contrib.auth.models import User

from api_v1.models import user_details  
from django.db.models import (Model, TextField, IntegerField, DateTimeField, BooleanField, ForeignKey,CASCADE)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class MessageModel(Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    user = ForeignKey(user_details, on_delete=CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = ForeignKey(user_details, on_delete=CASCADE, verbose_name='recipient',
                           related_name='to_user', db_index=True)
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    body = TextField()

    seen = BooleanField(default=False)

    liked = BooleanField(default=False)
    

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        #print("user.id {}".format(self.user.username))
        #print("user.id {}".format(self.recipient.username))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.username), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.username), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()


class likedStream(Model):
    user = ForeignKey(user_details, on_delete=CASCADE, verbose_name='user', null=True, blank=True , db_index=True)
    state = BooleanField(default=False)
    message = ForeignKey(MessageModel, on_delete=CASCADE, verbose_name='message', db_index=True)
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False, db_index=True)
    
    def __str__(self):
        return str(self.message)


    def notify_ws_clients(self):
        """
        Inform client there is a message is liked.
        """
        notification = {
            'type': 'push_liked',
            'liked': self.state,
            'message': '{}'.format(self.message.id)
        }

        channel_layer = get_channel_layer()
        #print("user.id {}".format(self.message.user.username))
        #print("user.id {}".format(self.message.recipient.username))

        async_to_sync(channel_layer.group_send)("{}".format(self.message.user.username), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.message.recipient.username), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        super(likedStream, self).save(*args, **kwargs)
        #if new is None: #send websoked even if message is disliked. 
        self.notify_ws_clients()




from django.core.serializers.json import DjangoJSONEncoder

class lastSeen(Model):
    user = ForeignKey(user_details, on_delete=CASCADE, verbose_name='user', null=True, blank=True , db_index=True)
    lastSeen = DateTimeField(editable=False, db_index=True)
    activeDevices = IntegerField(default=0)
    def __str__(self):
        return "{}, Active Devices- {}".format(self.user.username , self.activeDevices)

    def _isActive(self):
        if self.activeDevices < 1:
            return False
        else:
            return True

    def notify_ws_clients(self):
        """
        Inform client there is a message is liked.
        """
        if self.activeDevices < 1:
            notification = {
                'type': 'lastSeenUpdate',
                'chat': self.user.username,
                'activeNow': False,
                'lastSeen': str(self.lastSeen),
            }

        elif self.activeDevices == 1:
            notification = {
                'type': 'lastSeenUpdate',
                'chat': self.user.username,
                'activeNow': True,
                'lastSeen': str(self.lastSeen),
            }
        #print(notification)
        channel_layer = get_channel_layer()        
        latest_users = list(set(MessageModel.objects.filter(user=self.user).values_list('recipient', flat=True).order_by('pk')))
        for chat_user_pk in latest_users:
            try:
                chat_user = user_details.objects.get(pk = chat_user_pk)
                print("Notifing -" ,chat_user.username, end=' ')
                async_to_sync(channel_layer.group_send)("{}".format(chat_user.username), notification)
                #print("Success")

            except Exception as e:
                e = str(e)
                print(e)
                print("Failes to webhook recnent chat")

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        #print("Last Seen Updated")
        activeDevices = self.activeDevices
        from datetime import datetime
        self.lastSeen = datetime.now()
        super(lastSeen, self).save(*args, **kwargs)
        #print("last seen updated")
        #if new != None: #send websoked even if message is disliked. 
        #print(activeDevices)
        if activeDevices <= 1:
            self.notify_ws_clients()



class deviceLog(Model):
    user = ForeignKey(user_details, on_delete=CASCADE, verbose_name='user', null=True, blank=True , db_index=True)
    change = IntegerField(default=0)