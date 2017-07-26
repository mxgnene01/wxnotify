# -*- coding: utf-8 -*-

from wxnotify.common.app import WebApplication, run_app
from wxnotify.common.redis import RedisEngine
from wxnotify.common.postgres import PostgreSQLEngine
import wxnotify.apps.notify.services  # noqa
import wxnotify.apps.user.services  # noqa
import wxnotify.apps.message.services  # noqa
import logging

LOG = logging.getLogger('tornado.application')

RedisEngine.register_options()
PostgreSQLEngine.register_options('master')


class WechartNotifyServer(WebApplication):

    enabled_apps = ['wxnotify.apps.notify',
                    'wxnotify.apps.user',
                    'wxnotify.apps.message',
                    'wxnotify.apps.keepalive']

    def before_run(self, io_loop):
        LOG.info('starting wxnotify server ...')
        RedisEngine.start('master')
        PostgreSQLEngine.start('master')

def run():
    run_app(WechartNotifyServer)


if __name__ == '__main__':
    run()
