import pytest

from fbmsg import QuickReplyButton, QuickReply, Message


class TestQuickReplies:
    def test_QuickReplyButton(self):
        button = QuickReplyButton("title", "payload")
        assert button.to_dict() == {"title": "title", "payload": "payload"}
        with pytest.raises(TypeError):
            QuickReplyButton(1, "payload")
        with pytest.raises(TypeError):
            QuickReplyButton("title", None)

    def test_QuickReply(self):
        qr = QuickReply()
        with pytest.raises(TypeError):
            qr.add(1)
        button1 = QuickReplyButton("title", "payload")
        button2 = QuickReplyButton("title", "payload")
        qr.add(button1)
        qr.add(button2)
        assert qr.to_dict() == [
            {"title": "title", "payload": "payload"},
            {"title": "title", "payload": "payload"}
        ]


class TestMessage:
    def test_Message_without_QuickReply(self):
        msg = Message(text="text")
        assert msg.to_dict() == {"text": "text"}
        with pytest.raises(TypeError):
            Message(1)

    def test_Message_with_QuickReply(self):
        qr1 = QuickReply()
        button1 = QuickReplyButton("title1", "payload1")
        qr1.add(button1)
        msg = Message(text="text", quick_reply=qr1)

        assert msg.to_dict() == {
            "text": "text",
            "quick_replies": [{"title": "title1", "payload": "payload1"}]
        }
        with pytest.raises(TypeError):
            msg.set_quick_reply(1)

        with pytest.raises(TypeError):
            Message("Text", 1)

        qr2 = QuickReply()
        button2 = QuickReplyButton("title2", "payload2")
        qr2.add(button2)

        msg.set_quick_reply(qr2)
        assert msg.to_dict() == {
            "text": "text",
            "quick_replies": [{"title": "title2", "payload": "payload2"}]
        }
