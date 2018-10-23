

class MessengerClient:
    def __init__(self, page_token=None):
        if not isinstance(page_token, str):
            raise TypeError("page_token must be an instance of str")
        self.page_token = page_token
        self.message_processor = None
        self.postback_processor = None

    def register_message_processor(self):
        def add(processor):
            self.message_processor = processor
            return processor
        return add

    def register_postback_processor(self):
        def add(processor):
            self.postback_processor = processor
            return processor
        return add
    #
    # def process_json(self, msg_json):
    #     print(msg_json)
    #     return None
    #
    # def send_message(self):
    #     pass
    #
    # def set_persistent_menu(self):
    #     pass
