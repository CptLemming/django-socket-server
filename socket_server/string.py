import sys
from StringIO import StringIO

from .models import SocketLog


class SocketLoggerOut(StringIO):
    def write(self, s):
        SocketLog.objects.create(content=s)
        StringIO.write(self, 'Super %s' % s)
        sys.__stdout__.write('Sys Out %s' % s)


class SocketLoggerErr(StringIO):
    def write(self, s):
        SocketLog.objects.create(content=s)
        StringIO.write(self, s)
        sys.__stderr__.write(s)
