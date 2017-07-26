# -*- coding: utf-8 -*-
#

from tornado.options import (define as tornado_define,
                             options as tornado_options)
from urlparse import urlparse

import functools
import logging
import toredis.client

LOG = logging.getLogger('tornado.application')


class RedisConnectorError(Exception):
    pass


class RedisClient(toredis.client.Client):

    def connect(self, host='localhost', port=6379, callback=None):
        self._host = host
        self._port = port
        super(RedisClient, self).connect(host, port, callback)

    def on_disconnect(self):
        self.connect(self.host, self.port)


class RedisConnector(object):

    _instances = dict()

    @staticmethod
    def instance(name='master'):
        if name not in RedisConnector._instances:
            RedisConnector._instances[name] = RedisConnector()
        return RedisConnector._instances[name]

    @classmethod
    def client(cls):
        if not hasattr(cls, '_client') or not cls._client:
            raise RedisConnectorError('client not initialized')
        return cls._client

    @classmethod
    def connect(cls, uri, **kwd):
        LOG.info('connecting to redis server: %s' % uri)
        r = urlparse(uri)
        if r.scheme.lower() != 'redis':
            raise RedisConnectorError('uri should starts with redis://')
        client = RedisClient()
        client.connect(host=r.hostname, port=int(r.port or 6379))
        cls._client = client

        # r = urlparse(uri)
        # if r.scheme.lower() != 'redis':
        #     raise RedisConnectorError('uri should starts with redis://')
        # pool = RedisPool(host=r.hostname, port=int(r.port or 6379),
        #                  pool_size=tornado_options.redis_pool_size)
        # cls._pool = pool

class RedisEngine(object):

    @staticmethod
    def register_options(name='master'):
        opt_name = '' if name == 'master' else '-%s' % name
        tornado_define('redis%s-uri' % opt_name,
                       default='redis://127.0.0.1:6379',
                       group='%s redis' % name,
                       help="redis connection uri")
        tornado_define('redis%s-pool-size' % opt_name,
                       default=8,
                       group='%s redis' % name,
                       help="redis connection pool size")


    @staticmethod
    def start(name='master'):
        opt_name = '' if name == 'master' else '-%s' % name
        redis_settings = tornado_options.group_dict('%s redis' % name)
        instance = RedisConnector.instance(name)
        uri = redis_settings['redis%s-uri' % opt_name]
        RedisConnector.instance(name).connect(uri)


def with_redis(method=None, name="master"):

    def wrapper(function):

        @functools.wraps(function)
        def f(*args, **kwds):
            redis = RedisConnector.instance(name).client()
            return function(redis, *args, **kwds)
        return f

    return wrapper
