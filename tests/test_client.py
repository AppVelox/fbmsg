import pytest

from fbmsg.facebook_client import FacebookClient


class TestMessengerClient:
    def test_init(self):
        client = FacebookClient("Token")
        assert client.page_token == "Token"
        assert client.text_message_processor is None
        assert client.postback_processor is None

        with pytest.raises(TypeError):
            FacebookClient(1)

    def test_register_message_processor(self):
        client = FacebookClient("Token")

        @client.register_text_message_processor()
        def f():
            pass
        assert client.text_message_processor == f

    def test_register_postback_processor(self):
        client = FacebookClient("Token")

        @client.register_postback_processor()
        def f():
            pass
        assert client.postback_processor == f
