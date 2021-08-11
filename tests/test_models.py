#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-socket-server
------------

Tests for `django-socket-server` models module.
"""
from io import StringIO

from django.test import TestCase
from django.core.management import call_command

from socket_server.models import SocketLog


class TestSocket_server(TestCase):


    def test_model(self):
        log = SocketLog(content='test log entry')
        log.save()
        self.assertTrue(log)

    def test_command(self):
        out = StringIO()
        call_command('start_socket', stdout=out, test=0)
        self.assertTrue(True)
