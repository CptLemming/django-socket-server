# Django Socket Server

## Documentation
Add `socket_server` to `INSTALLED_APPS` in `settings.py`.

Create a `sockets.py` in an application of your project.

`django-socket-server` will discover the socket files that are in applications installed against Django.

An example `sockets.py` looks like this:

```
from socket_server.namespace import EventNamespace


class Namespace(EventNamespace):

    def client_connected(self, client):
        super(Namespace, self).client_connected(client)

        print 'Send ping'
        self.emit_to(client, 'ping')

    def register_callbacks(self):
        return {
            'pong': self.pong
        }

    def pong(self, client, **kwargs):
        print 'Received pong event'
```

Messages are send and received in JSON, and always contain an `event` key. This key is then mapped to callbacks, added inside `register_callbacks`.

You can specify a namespace name using the name property like so:

```
class Namespace(EventNamespace):
    name = 'pingpong'
```

If you do not specify a name, the app name will be used by default.

## Start Socket Server

Use the management command provided to start the socket server: `python manage.py start_socket`.

You may pass an optional `--port` to override the default port of `3000`.

## Client connection

The above example would expose the following: `ws://localhost:3000/pingpong`

## Links
- [Autobahn Python](https://github.com/tavendo/AutobahnPython)
- [Twisted](https://twistedmatrix.com/trac/)
