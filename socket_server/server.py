import json

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

from .exceptions import NamespaceNotFound


class SocketServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        self.path = request.path

    def getNamespace(self):
        return self.factory.getNamespace(self.path)

    def onOpen(self):
        try:
            namespace = self.getNamespace()
        except NamespaceNotFound:
            pass
        else:
            namespace.client_connected(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            # print("Binary message received: {0} bytes".format(len(payload)))
            pass
        else:
            try:
                namespace = self.getNamespace()
            except NamespaceNotFound:
                pass
            else:
                namespace.on_message(self, payload)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        try:
            namespace = self.getNamespace()
        except NamespaceNotFound:
            pass
        else:
            namespace.client_disconnected(self)

    def onClose(self, wasClean, code, reason):
        # namespaces = self.factory.getNamespaces()
        # for key in namespaces.keys():
        #     namespace = namespaces[key]
        #     namespace.on_stop(code, reason)
        pass


class SocketServerFactory(WebSocketServerFactory):
    protocol = SocketServerProtocol

    def __init__(self, *args, **kwargs):
        WebSocketServerFactory.__init__(self, *args, **kwargs)

        self.namespaces = {}

    def setNamespaces(self, namespaces):
        for key in namespaces.keys():
            self.namespaces[key] = namespaces[key](server=self)

    def getNamespace(self, namespace):
        if self.namespaces.get(namespace):
            return self.namespaces[namespace]
        else:
            raise NamespaceNotFound

    def getNamespaces(self):
        return self.namespaces
