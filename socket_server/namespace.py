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
                print 'An Error occurred calling event [%s]' % event
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


class RoomMixin(EventMixin):

    def __init__(self, server):
        super(RoomMixin, self).__init__(server)
        self.rooms = {}

    def register_callbacks(self):
        callbacks = super(RoomMixin, self).register_callbacks()
        callbacks.update({
            'room/create': self.create_room,
            'room/destroy': self.destroy_room,
            'room/join': self.join_room,
            'room/leave': self.leave_room,
            'room/broadcast': self.broadcast_room,
            'room/peers': self.get_room_peers,
        })

        return callbacks

    def create_room(self, client, **kwargs):
        name = kwargs.get('name')
        join = kwargs.get('join', False)

        if name and name not in self.rooms:
            self.rooms[name] = {'name': name, 'clients': {}}
            self.emit_to(client, 'room/created', name=name)

        if join:
            self.join_room(client, name=name)

    def destroy_room(self, client, **kwargs):
        name = kwargs.get('name')

        if name and name in self.rooms:
            for key in self.rooms[name]['clients'].keys():
                room_client = self.rooms[name]['clients'][key]
                self.leave_room(room_client, name=name)
            del self.rooms[name]
            self.emit_to(client, 'room/destroyed', name=name)
        else:
            self.emit_to(client, 'room/error', message='Room %s does not exist' % name)

    def get_room_peers(self, client, **kwargs):
        name = kwargs.get('name')

        if name and name in self.rooms:
            clients = []
            for key in self.rooms[name]['clients'].keys():
                room_client = self.rooms[name]['clients'][key]
                clients.append(room_client.peer)
            self.emit_to(client, 'room/peers', peers=clients)
        else:
            self.emit_to(client, 'room/error', message='Room %s does not exist' % name)

    def join_room(self, client, **kwargs):
        name = kwargs.get('name')

        if name and name in self.rooms and not self.rooms[name]['clients'].get(client.peer):
            self.rooms[name]['clients'][client.peer] = client
            self.emit_to(client, 'room/joined', name=name)
        else:
            self.emit_to(client, 'room/error', message='Room %s does not exist' % name)

    def leave_room(self, client, **kwargs):
        name = kwargs.get('name')
        respond = kwargs.get('respond', True)

        if name and name in self.rooms and self.rooms[name]['clients'].get(client.peer):
            del self.rooms[name]['clients'][client.peer]
            if respond:
                self.emit_to(client, 'room/left', name=name)

    def broadcast_room(self, client, **kwargs):
        name = kwargs.get('name')
        payload = kwargs.get('payload')
        exclude = kwargs.get('exclude', True)

        if name and name in self.rooms:
            for key in self.rooms[name]['clients'].keys():
                room_client = self.rooms[name]['clients'][key]
                if not exclude or room_client.peer != client.peer:
                    self.emit_to(
                        room_client, 'room/broadcast', name=name, payload=payload)
        else:
            self.emit_to(client, 'room/error', message='Room %s does not exist' % name)
