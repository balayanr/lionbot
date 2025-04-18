from lionbot.vendors.cycling.peloton import client
from . import mock_responses

class MockSession(client._PelotonAPISession):
    def _login(self):
        pass

    def request(self, method, *args, headers: dict | None = None, **kwargs):
        return mock_responses.RESPONSES.get(method)