from django.db import models
from communities.models import Communities
from account.models import Account
# Create your models here.
from channels.auth import AuthMiddlewareStack, CookieMiddleware
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from account.models import Token


class Message(models.Model):
    community = models.ForeignKey(Communities, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, null=False)
    time = models.DateTimeField(verbose_name='date time', auto_now_add=True)

    # @property
    # def community_name(self):
    #     return self.community.name


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        # url = scope['url_route']['kwargs']['room_name']
        # print(headers)
        # print(scope)
        # print(headers[b'sec-websocket-protocol'])
        if b'sec-websocket-protocol' in headers:
            # print('YYYYYYYYYYYY')
            try:
                token_key = headers[b'sec-websocket-protocol'].decode()
                # print("Token : "+token_key)
                # if token_name == 'Token':
                token = Token.objects.get(key=token_key)
                print("HHHHH")
                scope['user'] = token.user
                # self.base_send({"type": "websocket.accept", "subprotocol": token_key})
                close_old_connections()
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        return self.inner(scope)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
