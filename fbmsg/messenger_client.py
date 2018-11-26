import json

import requests

from .models.incoming import Request
from .models.messages import Message


class MessengerClient:

    def __init__(self, page_token: str = None):
        if not isinstance(page_token, str):
            raise TypeError("page_token must be an instance of str")
        self.page_token = page_token
        self.text_message_processor = None
        self.postback_processor = None
        self.fb_url = f'https://graph.facebook.com/v2.6/me/{"{}"}?access_token={page_token}'

    def register_text_message_processor(self):
        def add(processor: function):
            self.message_processor = processor
            return processor

        return add

    def register_postback_processor(self):
        def add(processor: function):
            self.postback_processor = processor
            return processor

        return add

    def process_json(self, msg_json: dict):
        if not isinstance(msg_json, dict):
            raise TypeError('msg_json must be an instance of dict')
        if 'entry' not in msg_json:
            raise ValueError("Malformed incoming request from Facebook")
        request = Request(**msg_json)
        # for entry in msg_json['entry']:
        #     message = IncomingMessage(entry)
        #
        #     if message.type == IncomingMessage.TEXT_MESSAGE:
        #         self.text_message_processor(message)
        #     elif message.type == IncomingMessage.POSTBACK_MESSAGE:
        #         self.postback_processor(message)
        #     else:
        #         raise ValueError("Unknown message type")

        return

    def send_message(self, recipient_id: int, message: Message):
        if not isinstance(message, Message):
            raise TypeError('message must be an instance of Message')
        if not isinstance(recipient_id, int):
            raise TypeError('recipient_id must be an instance of int')
        resr = self.post_request('messages',
                                 json.dumps({'message': message.to_dict(), 'recipient': {'id': recipient_id}}))

    def post_request(self, endpoint: str, data: str):
        if not isinstance(endpoint, str):
            raise TypeError('endpoint must be an instance of str')
        if not isinstance(data, str):
            raise TypeError('data must be an instance of str')
        response = requests.post(self.fb_url.format(endpoint), data=data)
        response.raise_for_status()
        return json.loads(response.text)

    #
    #
    # def set_persistent_menu(self):
    #     pass
