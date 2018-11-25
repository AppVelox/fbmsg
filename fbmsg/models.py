




class IncomingMessage:
    TEXT_MESSAGE = 1
    POSTBACK_MESSAGE = 2

    def __init__(self, msg_json):
        message_data = msg_json['messaging'][0]

        self.sender_id = message_data['sender']['id']
        self.recipient_id = message_data['recipient']['id']
        self.type = IncomingMessage.TEXT_MESSAGE
