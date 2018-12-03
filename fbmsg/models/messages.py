class QuickReplyButton:
    def __init__(self, title: str, type: str, **kwargs):
        if not isinstance(title, str):
            raise TypeError("QuickReplyButton.title must be an instance of str")
        if not isinstance(type, str):
            raise TypeError("QuickReplyButton.type must be an instance of str")

        self.title = title
        self.type = type
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def to_dict(self):
        return dict(vars(self))


class QuickReply:
    def __init__(self):
        self.buttons = []

    def add(self, button: QuickReplyButton):
        if not isinstance(button, QuickReplyButton):
            raise TypeError("button must be an instance of QuickReplyButton")
        self.buttons.append(button)

    def to_dict(self):
        return [button.to_dict() for button in self.buttons]


class Message:
    def __init__(self, text: str, quick_reply: QuickReply = None):
        if not isinstance(text, str):
            raise TypeError("Message.text must be an instance of str")
        if quick_reply and not isinstance(quick_reply, QuickReply):
            raise TypeError("Message.quick_reply must be an instance of QuickReply")
        self.text = text
        self.quick_reply = quick_reply

    def set_quick_reply(self, quick_reply):
        if not isinstance(quick_reply, QuickReply):
            raise TypeError("Message.quick_reply must be an instance of QuickReply")
        self.quick_reply = quick_reply

    def to_dict(self):
        msg = {"text": self.text}
        if self.quick_reply:
            msg['quick_replies'] = self.quick_reply.to_dict()
        return msg
