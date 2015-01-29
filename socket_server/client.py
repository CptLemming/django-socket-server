import json

from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory


class SocketClientProtocol(WebSocketClientProtocol):

    def emit(self, event_name, **kwargs):
        payload = self._format_outbound_data(event_name, **kwargs)

        self.sendMessage(payload)

    def _format_outbound_data(self, event, **kwargs):
        """ Format outbound message as JSON """
        message = {'event': event}

        for key in kwargs.keys():
            message[key] = kwargs.get(key)

        return json.dumps(message).encode('utf8')

    def onMessage(self, payload, isBinary):
        self.factory.handle_message(self, payload)


class BaseSocketClientFactory(WebSocketClientFactory):
    protocol = SocketClientProtocol

    def __init__(self, *args, **kwargs):
        WebSocketClientFactory.__init__(self, *args, **kwargs)

        self.callbacks = {}
        self.register_callbacks()

    def register_callbacks(self):
        pass

    def on(self, event_name, callback):
        self.callbacks[event_name] = callback

    def fire_callback(self, client, event_name, **kwargs):
        if event_name in self.callbacks:
            self.callbacks[event_name](client, **kwargs)

    def handle_message(self, client, message):
        payload = self.parse_message(message)

        if payload:
            event = payload.pop('event')
            self.fire_callback(client, event, **payload)

    def parse_message(self, message):
        payload = json.loads(message)

        if 'event' in payload:
            output = payload
            return output
