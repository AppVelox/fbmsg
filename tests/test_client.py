import pytest

from fbmsg.messenger_client import MessengerClient


class TestMessengerClient:
    def test_init(self):
        client = MessengerClient("Token")
        assert client.page_token == "Token"
        assert client.message_processor is None
        assert client.postback_processor is None

        with pytest.raises(TypeError):
            MessengerClient(1)

    def test_register_message_processor(self):
        client = MessengerClient("Token")

        @client.register_message_processor()
        def f():
            pass
        assert client.message_processor == f

    def test_register_postback_processor(self):
        client = MessengerClient("Token")

        @client.register_postback_processor()
        def f():
            pass
        assert client.postback_processor == f
