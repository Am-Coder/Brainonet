from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from groupchat.models import Message
from account.models import Token
from communities.models import Communities, CommunitySubscribers
from django.shortcuts import Http404
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        logger.info("Men Have Meet")
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
            logger.info("MEN left")
            await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(self.scope)
        # message = text_data_json['message']
        auth = text_data_json['auth']
        if auth:
            logger.info("Authenticating")
            token = text_data_json['token']
            await self.validate_token(token)
        else:
            if self.scope['user']:
                logger.info("WebSocketRecieve = " + text_data_json['message'])
                await self.message_save_utility(
                    self.scope['token'],
                    self.scope['url_route']['kwargs']['room_name'],
                    text_data_json['message']
                )

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': text_data_json['message']
                    }
                )
            else:
                await self.close()

    # Handler to Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        logger.info("Recieved = "+message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def message_save_utility(self, token, communityname, content):
        try:
            user = Token.objects.get(key=token).user
            community = Communities.objects.get(name=communityname)
            CommunitySubscribers.objects.get(user=user, community=community)
            message = Message(user=user, content=content, community=community)
            message.save()

        # These conditions need to be prechecked
        except Token.DoesNotExist:
            raise Http404(" Authentication Failed ")
        except Communities.DoesNotExist:
            raise Http404(" Community Does Not Exist ")
        except CommunitySubscribers.DoesNotExist:
            raise Http404(" You have not subscribed to this community ")

    @database_sync_to_async
    def validate_token(self, token):
        try:
            token = Token.objects.get(key=token)
            logger.info("Token Verification Done")
            self.scope['user'] = token.user
            self.scope['token'] = token
        except Token.DoesNotExist:
            logger.info("Verification Failed")
            self.scope['user'] = None


