from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from groupchat.models import Message
from account.models import Token
from communities.models import Communities
from django.shortcuts import Http404
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print("XXXXX")
        # print(self.scope)
        # token_key = self.scope['headers'][b'sec-websocket-protocol'].decode()
        # print(self.scope['headers'][-1][1].decode())
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # self.base_send({"type": "websocket.accept", "subprotocol": token_key})
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print("disconnect")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("WebSocketRecieve = " + message)
        print(self.scope)
        # Send message to room group
        token = self.scope['url_route']['kwargs']['token']
        if token:
            self.message_save_utility(
                token,
                self.scope['url_route']['kwargs']['room_name'],
                message
            )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Handler to Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print("Recieved = "+message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    # @database_sync_to_async
    def message_save_utility(self, token, communityname, content):
        try:
            user = Token.objects.get(key=token).user
            community = Communities.objects.get(name=communityname)
            message = Message(user=user, content=content, community=community)
            message.save()

        # These conditions need to be prechecked
        except Token.DoesNotExist:
            raise Http404(" Authentication Failed ")
        except Communities.DoesNotExist:
            raise Http404(" Community Does Not Exist ")
