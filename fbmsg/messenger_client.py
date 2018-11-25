from fbmsg.models import IncomingMessage


class MessengerClient:
    def __init__(self, page_token: str=None):
        if not isinstance(page_token, str):
            raise TypeError("page_token must be an instance of str")
        self.page_token = page_token
        self.text_message_processor = None
        self.postback_processor = None

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
        for entry in msg_json['entry']:
            message = IncomingMessage(entry)

            if message.type == IncomingMessage.TEXT_MESSAGE:
                self.text_message_processor(message)
            elif message.type == IncomingMessage.POSTBACK_MESSAGE:
                self.postback_processor(message)
            else:
                raise ValueError("Unknown message type")

        return


    #
    # def send_message(self):
    #     pass
    #
    # def set_persistent_menu(self):
    #     pass
