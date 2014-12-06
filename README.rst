=============================
django-socket-server
=============================

.. image:: http://img.shields.io/travis/CptLemming/django-socket-server.svg?style=flat-square
    :target: https://travis-ci.org/CptLemming/django-socket-server/

.. image:: http://img.shields.io/pypi/v/django-socket-server.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-socket-server/
    :alt: Latest Version

.. image:: http://img.shields.io/pypi/dm/django-socket-server.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-socket-server/
    :alt: Downloads

.. image:: http://img.shields.io/pypi/l/django-socket-server.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-socket-server/
    :alt: License

.. image:: http://img.shields.io/coveralls/CptLemming/django-socket-server.svg?style=flat-square
  :target: https://coveralls.io/r/CptLemming/django-socket-server?branch=master

Django Socket Server

Quickstart
----------

1. Install `django-socket-server`::

    pip install django-socket-server

2. Add `socket_server` to `INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...
        'socket_server',
        ...
    )

Create a `sockets.py` in an application of your project.

`django-socket-server` will discover the socket files that are in applications installed against Django.

An example `sockets.py` looks like this::

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


Messages are sent and received in JSON, and always contain an `event` key. This key is then mapped to callbacks, added inside `register_callbacks`.

You can specify a namespace name using the name property like so::

    class Namespace(EventNamespace):
        name = 'pingpong'


If you do not specify a name, the app name will be used by default.

Start Socket Server
-------------------

Use the management command provided to start the socket server: `python manage.py start_socket`.

You may pass an optional `--port` to override the default port of `3000`.

Client connection
-----------------

The above example would expose the following: `ws://localhost:3000/pingpong`


Documentation
-------------

The full documentation is at https://django-socket-server.readthedocs.org.

Links
-----

- [Autobahn Python](https://github.com/tavendo/AutobahnPython)
- [Twisted](https://twistedmatrix.com/trac/)
