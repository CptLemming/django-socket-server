import json


class BaseNamespace(object):
    name = None

    def __init__(self, server):
        self.server = server
        self.clients = []
        super(BaseNamespace, self).__init__()

    def get_name(self):
        """ Get namespace name """
        return self.name

    def _register_client(self, client):
        """ Add client to list of connected clients """
        self.clients.append(client)

    def _unregister_client(self, client):
        """ Remove client from list of connected clients """
        self.clients.remove(client)

    def on_start(self, client):
        """ Client starts connection """
        pass

    def client_connected(self, client):
        """ Client connected """
        self._register_client(client)

    def on_stop(self, code, reason):
        """ Server stopped """
        pass

    def client_disconnected(self, client):
        """ Client disconnected """
        self._unregister_client(client)

    def on_message(self, client, message):
        """ Message received from client """
        pass

    def _format_outbound_data(self, message):
        """ Ensure character encoding """
        return message.encode('utf8')

    def emit(self, message):
        """ Send message to all connected clients """
        data = self._format_outbound_data(message)
        for client in self.clients:
            client.sendMessage(data)

    def emit_to(self, client, message):
        """ Send message to single client """
        data = self._format_outbound_data(message)
        client.sendMessage(data)

    def emit_except(self, client, message):
        """ Send message to all clients except single """
        data = self._format_outbound_data(message)
        for client_connected in self.clients:
            if client != client_connected:
                client.sendMessage(data)


class EventMixin(object):

    def __init__(self, server):
        super(EventMixin, self).__init__(server)
        self.callbacks = self.register_callbacks()

    def register_callbacks(self):
        return {}

    def _handle_inbound_message(self, client, message):
        """ Take an inbound message, parse and fire any callbacks """
        payload = self._parse_inbound_message(message)
        if payload:
            event = payload.pop('event')
            self._fire_callback(client, event, **payload)

    def _fire_callback(self, client, event, **kwargs):
        """ Check for registered callbacks and fire """
        if event in self.callbacks:
            try:
                self.callbacks[event](client, **kwargs)
            except TypeError:
                pass

    def _parse_inbound_message(self, message):
        """ Parse inbound JSON message """
        payload = json.loads(message)

        if 'event' in payload:
            output = payload
            return output

    def on_message(self, client, message):
        """ Message received from client """
        self._handle_inbound_message(client, message)

    def _format_outbound_data(self, event, **kwargs):
        """ Format outbound message as JSON """
        message = {'event': event}

        for key in kwargs.keys():
            message[key] = kwargs.get(key)

        return json.dumps(message).encode('utf8')

    def emit(self, event, **kwargs):
        """ Send message to all connected clients """
        data = self._format_outbound_data(event, **kwargs)
        for client in self.clients:
            client.sendMessage(data)

    def emit_to(self, client, event, **kwargs):
        """ Send message to single client """
        data = self._format_outbound_data(event, **kwargs)
        client.sendMessage(data)

    def emit_except(self, client, event, **kwargs):
        """ Send message to all clients except single """
        data = self._format_outbound_data(event, **kwargs)
        for client_connected in self.clients:
            if client != client_connected:
                client.sendMessage(data)
