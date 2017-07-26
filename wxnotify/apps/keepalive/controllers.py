#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This piece of code is written by
#    Meng xiangguo <mxgnene01@gmail.com>
# with love and passion!
#
#        H A P P Y    H A C K I N G !
#              _____               ______
#     ____====  ]OO|_n_n__][.      |    |]
#    [________]_|__|________)<     |MENG|
#     oo    oo  'oo OOOO-| oo\_   ~o~~~o~'
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                        2017/7/24  下午5:55

from wxnotify.common.route import route
from wxnotify.common import controller
from tornado.web import StaticFileHandler, RequestHandler
from os.path import join as path_join, exists as file_exists
import os


@route('/heartbeat.html')
class HeartbeatController(RequestHandler):

    SUPPORTED_METHODS = ('GET', 'HEAD')

    def head(self):
        self.finish('service ok')

    def get(self):
        self.finish('service ok')


@route('/healthcheck.html')
class HealthCheckController(StaticFileHandler):

    path = os.getcwd()
    default_filename = 'healthcheck.html'

    def get(self, path=None, include_body=True):
        if not file_exists(path_join(self.path, self.default_filename)):
            self.set_status(404)
            self.finish("")
        else:
            super(HealthCheckController, self).get(self.default_filename,
                                                   include_body)

    def head(self, path=None):
        if not file_exists(path_join(self.path, self.default_filename)):
            self.set_status(404)
            self.finish("")
        else:
            super(HealthCheckController, self).head(self.default_filename)
