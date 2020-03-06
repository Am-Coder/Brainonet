from twilio.rest import Client


class TwilioService:
    __account_sid = 'ACd806b6f607a4f1bf4a0269d1de82a467'
    __auth_token = 'd1cb6fe665f6717addf0a46652cc0e1d'
    __my_number = '+17014012651'
    __client = None

    def __init__(self):
        self.__client = Client(self.__account_sid, self.__auth_token)

    def send(self, msg, receiver):
        message = self.__client.messages.create(
            body=msg,
            from_=self.__my_number,
            to=receiver
        )
        return message.status
        # print(message.sid)
