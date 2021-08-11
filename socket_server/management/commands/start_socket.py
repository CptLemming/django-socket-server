import os
import sys
import time
import signal
from importlib import import_module

from django.core.management.base import BaseCommand
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
    
    def add_arguments(self, parser):
        parser.add_argument('--test',action='store_true',help='Start server and close it')
    
    def handle(self, *args, **options):
        options.update({'port': 3000})
        print('Listening on port localhost:%s' % options['port'])

        import sys

        from twisted.python import log
        from twisted.internet import reactor

        log.startLogging(sys.stdout)

        factory = SocketServerFactory("ws://localhost:%s" % options['port'])
        factory.setNamespaces(namespaces)

        reactor.listenTCP(options['port'], factory)
        if 'test' in options and options['test']:
            r = os.fork()
            if r == 0:
                reactor.run()
            else:
                os.kill(r, signal.SIGKILL)
                os.waitpid(r,0)
        else:
            reactor.run()
