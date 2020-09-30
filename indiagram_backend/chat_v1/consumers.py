
# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import lastSeen, deviceLog
from api_v1.models import user_details
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.db.models import Count, F, Value
from django.db.models import Sum


from .models import lastSeen
lastSeen.objects.all().update(activeDevices=0)
deviceLog.objects.all().delete()

print("Active devices reseted!")

def logChange(self, change):
    user = user_details.objects.get(username=self.username)
    deviceLog.objects.create(user=user, change=change)

def updateLastSeen(self):
        user = user_details.objects.get(username=self.username)
        log = deviceLog.objects.all().filter(user=user).aggregate(Sum('change'))
        devices = log["change__sum"]
        print(user, "Devices - " , devices)

        lastseen_object = lastSeen.objects.get(user=user)
        lastseen_object.activeDevices = devices
        lastseen_object.save()
        
        '''
        obj, created = lastSeen.objects.update_or_create(user=user, defaults={'user': user, 'activeDevices': change },)
        '''
        return True

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        # Join room group

        await self.channel_layer.group_add(
            self.username,
            self.channel_name
        )
        status = await database_sync_to_async(logChange)(self, change=1)
        status = await database_sync_to_async(updateLastSeen)(self)

        #print(status)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        status = await database_sync_to_async(logChange)(self, change=-1)
        status = await database_sync_to_async(updateLastSeen)(self)

        #print(status)

        await self.channel_layer.group_discard(
            self.username,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None,bytes_data = None):
        text_data_json = json.loads(text_data)
        target = text_data_json['target']
        ws_type = text_data_json['type']
        
        info = {
                'type': ws_type,
                'target': target
            }

        if ws_type == "typing":    
            channel_layer = get_channel_layer()
            await channel_layer.group_send("{}".format(target), info)
        else:
            # Send message to room group
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': ws_type,
                    'target': target
                }
            )

    async def recieve_group_message(self, event):
        message = event['message']
        ##print(event)
        # Send message to WebSocket
        await self.send(
             text_data=json.dumps({
            'type': 'recive_message',     
            'message': message,
        }))

    async def push_liked(self, event):
        message = event['message']
        liked = event['liked']
        ##print(event)
        # Send message to WebSocket
        await self.send(
             text_data=json.dumps({
            'type': 'liked',     
            'message': message,
            'liked': liked
        }))

    async def push_seen(self, event):
        seen = event['seen']
        upto_id = event['upto_id']
        chat = event['chat']

        ##print(event)
        # Send message to WebSocket
        await self.send(
             text_data=json.dumps({
            'type': 'seen',     
            'chat': chat,     
            'seen': seen,
            'upto_id': upto_id
        }))    

    async def lastSeenUpdate(self, event):
        lastSeen = event['lastSeen']
        activeNow = event['activeNow']
        chat = event['chat']

        ##print(event)
        # Send message to WebSocket
        await self.send(
             text_data=json.dumps({
            'type': 'active',     
            'chat': chat,     
            'activeNow': activeNow,
            'lastSeen': lastSeen,     
        }))        

    async def typing(self, event):
        #key = event['key']
        target = event['target']
        #print(target, " typing")
        ##print(event)
        # Send message to WebSocket

        await self.send(
             text_data=json.dumps({
            'type': 'typing',     
            'chat': target,     
        }))            