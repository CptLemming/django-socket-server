from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils.importlib import import_module
from django.conf import settings

from socket_server.server import SocketServerFactory

namespaces = dict()

for app in settings.INSTALLED_APPS:
    try:
        sockets = import_module('%s.sockets' % app, 'sockets')
    except ImportError:
        pass
    else:
        Namespace = sockets.Namespace
        if getattr(Namespace, 'name'):
            name = Namespace.name
        else:
            name = app.split('.')[-1]
        Namespace.name = name
        namespaces['/' + name] = Namespace


class Command(BaseCommand):
    """
    Start the socket server and attach listeners.
    """
    help = 'Start a websocket server'

    # option_list = BaseCommand.option_list + (
    #     make_option(
    #         '--port',
    #         action='store',
    #         dest='port',
    #         default=3000,
    #         type='int',
    #         help='Port used for incomings websocket requests default to 3000',)
    # )

    def handle(self, *args, **options):
        options.update({'port': 3000})
        print 'Listening on port localhost:%s' % options['port']

        import sys

        from twisted.python import log
        from twisted.internet import reactor

        log.startLogging(sys.stdout)

        factory = SocketServerFactory("ws://localhost:%s" % options['port'], debug=False)
        factory.setNamespaces(namespaces)

        reactor.listenTCP(options['port'], factory)
        reactor.run()
