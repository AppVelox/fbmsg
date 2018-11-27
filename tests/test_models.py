import pytest

from fbmsg.models.messages import QuickReply, QuickReplyButton, Message
from fbmsg.models.incoming import Request, Entry, Message as iMessage, QuickReply as iQuickReply
from fbmsg.models.settings import Analytics, MenuItem, PersistentMenu


class TestQuickReplies:
    def test_QuickReplyButton(self):
        button = QuickReplyButton("title", "payload")
        assert button.to_dict() == {'content_type': 'text', "title": "title", "payload": "payload"}
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
            {'content_type': 'text', "title": "title", "payload": "payload"},
            {'content_type': 'text', "title": "title", "payload": "payload"}
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
            "quick_replies": [{'content_type': 'text', "title": "title1", "payload": "payload1"}]
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
            "quick_replies": [{'content_type': 'text', "title": "title2", "payload": "payload2"}]
        }


class TestIncoming:
    def test_QuickReply(self):
        with pytest.raises(TypeError):
            iQuickReply(1)
        qr = iQuickReply('test')
        assert qr.payload == 'test'

    def test_Message(self):
        with pytest.raises(TypeError):
            iMessage('', {}, 1, {})
        with pytest.raises(TypeError):
            iMessage({}, 1, 1, {})
        with pytest.raises(TypeError):
            iMessage({}, {}, '', {})
        with pytest.raises(TypeError):
            iMessage({}, {}, 1, 1)
        m = iMessage(**{'sender': {'id': '1169720893152609'}, 'recipient': {'id': '2278924455579804'},
                        'timestamp': 1543226751645,
                        'message': {'mid': 'test', 'seq': 15, 'text': 'test', 'quick_reply': {'payload': 'test'}}})

    def test_Entry(self):
        with pytest.raises(TypeError):
            Entry(1, 1, [])
        with pytest.raises(TypeError):
            Entry('', '', [])
        with pytest.raises(TypeError):
            Entry('', 1, 1)
        Entry('test', 1, [{'sender': {'id': '1169720893152609'}, 'recipient': {'id': '2278924455579804'},
                           'timestamp': 1543226751645,
                           'message': {'mid': 'test', 'seq': 15, 'text': 'test', 'quick_reply': {'payload': 'test'}}}])

    def test_Request(self):
        with pytest.raises(TypeError):
            Request(1, [])
        with pytest.raises(TypeError):
            Request('', '')
        Request('', [{'id': '2278924455579804', 'time': 1543226752083, 'messaging': [
            {'sender': {'id': '1169720893152609'}, 'recipient': {'id': '2278924455579804'}, 'timestamp': 1543226751645,
             'message': {
                 'mid': 'OqcEBjJm5yIB4FXOi-QQNpkHi9Y8onq4GJ-SGf1uuw59FAZJh1mi1w5xENFgluiJNdemXElPHwwrWElCYLW26g',
                 'seq': 15, 'text': 'heloo'}}]}])


class TestSettings:
    def test_MenuItem(self):
        i = MenuItem(**{
            "title": "Pay Bill",
            "type": "postback",
            "payload": "PAYBILL_PAYLOAD"
        })
        with pytest.raises(TypeError):
            MenuItem(1, '')
        with pytest.raises(TypeError):
            MenuItem('', 1)
        assert i.to_dict() == {
            "title": "Pay Bill",
            "type": "postback",
            "payload": "PAYBILL_PAYLOAD"
        }

    def test_PersistentMenu(self):
        with pytest.raises(TypeError):
            PersistentMenu(1, '', False)
        with pytest.raises(TypeError):
            PersistentMenu([], 1, False)
        with pytest.raises(TypeError):
            PersistentMenu([], '', 1)
        m = PersistentMenu()
        i = MenuItem(**{
            "title": "Pay Bill",
            "type": "postback",
            "payload": "PAYBILL_PAYLOAD"
        })
        m.add(i)
        assert m.to_dict() == {'locale': 'default', 'composer_input_disabled': False, 'call_to_actions': [
            {'type': 'postback', 'title': 'Pay Bill', 'payload': 'PAYBILL_PAYLOAD'}]}

    def test_Analytics(self):
        a = Analytics([], 123, 123)
        assert a.to_dict() == {
            'custom_events': [],
            'page_id': 123,
            'page_scoped_user_id': 123,
            'event': 'CUSTOM_APP_EVENTS',
            'advertiser_tracking_enabled': True,
            'application_tracking_enabled': True,
            'extinfo': ['mb1'],
        }
