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

from wxnotify.common.redis import with_redis
from tornado.gen import coroutine, Task, Return
from tornado.httpclient import AsyncHTTPClient
from tornado.options import (options as tornado_options,
                             define as tornado_define)
import logging
import json

tornado_define('appid',
               default='',
               help='wx appid ')

tornado_define('secret',
               default='',
               help='wx secret')

tornado_define('access_token_expire',
               default=700,
               help='access_token expire time')

tornado_define('template_id',
               default='slDvEon80wxgJHJ7oue9jIp4y7UyS2TEAsgSmJQLpJE',
               help='template id')

tornado_define('get_access_token_url',
               default='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}',
               help='get wx access_token url')

tornado_define('send_push_url',
               default='https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={0}',
               help='push url')

BIZLOG = logging.getLogger("wxnotify.business")


def wxnotify_key(appid):
    return 'wxnotify_%s' % appid


@coroutine
def get_access_token():
    client = AsyncHTTPClient()
    resp = yield client.fetch(tornado_options.get_access_token_url.format(tornado_options.appid, tornado_options.secret))
    access_token = json.loads(resp.body).get('access_token')

    raise Return(access_token)


@coroutine
@with_redis('master')
def set_access_token(redis, appid, access_token):
    pipeline = redis.pipeline()
    pipeline.set(wxnotify_key(appid), access_token)
    pipeline.expire(wxnotify_key(appid), tornado_options.access_token_expire)
    ret = yield Task(pipeline.send)

    BIZLOG.debug("set redis returns: %s" % ret)
    if ret[0] == 'OK' and ret[1] == 1:
        BIZLOG.debug("access_token code saved")
        raise Return(True)
    else:
        raise Return(False)


@coroutine
@with_redis('master')
def find_access_token(redis):

    access_token = yield Task(redis.get, wxnotify_key(tornado_options.appid))

    if access_token is None or access_token == '':
        access_token = yield get_access_token()
        ret = yield set_access_token(tornado_options.appid, access_token)
        if not ret:
            raise Return('None')

    raise Return(access_token)


@coroutine
def send_notify(openid, title, time, machine, moniterkey, state, output, remark, url):
    client = AsyncHTTPClient()
    params = {
        'touser': openid,
        'template_id': tornado_options.template_id,
        'url': url,
        'data': {
            'first': {
                'value': '%s\n' % title,
                'color': '#FF0000'
            },
            'keyword1': {
                'value': time,
                'color': '#173177'
            },
            'keyword2': {
                'value': machine,
                'color': '#173177'
            },
            'keyword3': {
                'value': moniterkey,
                'color': '#173177'
            },
            'keyword4': {
                'value': state,
                'color': '#173177'
            },
            'keyword5': {
                'value': output,
                'color': '#173177'
            },
            'remark': {
                'value': remark,
                'color': '#173177'
            }
        }
    }

    access_token = yield find_access_token()
    if access_token is None:
        raise Return(False)

    try:
        resp = yield client.fetch(tornado_options.send_push_url.format(access_token),
                                  method='POST',
                                  raise_error=True,
                                  body=json.dumps(params),
                                  connect_timeout=3.0,
                                  request_timeout=3.0,
                                  follow_redirects=True,
                                  allow_nonstandard_methods=True
                                  )
    except Exception, e:
        BIZLOG.error(e)


    BIZLOG.debug("wechat gateway returns: [%s]%s" % (resp.code, resp.body))
    if resp.code == 200:
        raise Return((True, resp.body))
    else:
        raise Return((False, resp.body))
