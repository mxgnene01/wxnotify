#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Meng xiangguo <mxgnene01@gmail.com>
#
#              _____               ______
#     ____====  ]OO|_n_n__][.      |    |]
#    [________]_|__|________)<     |MENG|
#     oo    oo  'oo OOOO-| oo\_   ~o~~~o~'
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                        2017/7/21  下午4:01

from tornado.gen import coroutine, Task, Return
from tornado.httpclient import AsyncHTTPClient
from tornado.options import (options as tornado_options,
                             define as tornado_define)
from wxnotify.apps.notify.services import find_access_token
import logging
import json
from wxnotify.common.postgres import with_postgres
from wxnotify.common.redis import with_redis
from wxnotify.common.database import fetchone_as_dict

tornado_define('get_user_list_url',
               default='https://api.weixin.qq.com/cgi-bin/user/get?access_token={0}&next_openid={1}',
               help='get user list url, 一次拉取调用最多拉取10000个关注者的OpenID')

tornado_define('get_user_detail_url',
               default='https://api.weixin.qq.com/cgi-bin/user/info?access_token={0}&openid={1}&lang=zh_CN ',
               help='get user detail url')

BIZLOG = logging.getLogger("wxnotify.business")


def redis_key(key):
    return 'wx_username:%s' % key


@coroutine
def get_user_info(user_name):
    openid = yield get_user_info_from_redis(user_name)
    if not openid:
        data = yield get_user_info_from_db(user_name)
        openid = data.get('openid')
        if data:
            yield save(user_name, openid)

    raise Return(openid)

@coroutine
@with_redis('master')
def get_user_info_from_redis(redis, user_name):
    openid = yield Task(redis.get, redis_key(user_name))
    raise Return(openid)


@coroutine
@with_postgres('master')
def get_user_info_from_db(db, user_name):
    c = yield db.execute("select openid from dl_user_weixin where user_name = '%s'" % user_name)
    openid = fetchone_as_dict(c)

    raise Return(openid)

@coroutine
@with_redis('master')
def save(redis, user_name, openid):
    pipeline = redis.pipeline()
    pipeline.set(redis_key(user_name), openid)
    pipeline.expire(redis_key(user_name), 86400)
    ret = yield Task(pipeline.send)

    BIZLOG.debug("set redis returns: %s" % ret)
    if ret[0] == 'OK':
        BIZLOG.info("openid code saved")
        raise Return(True)
    else:
        raise Return(False)


@coroutine
def get_user_list():
    '''
    返回所有关注用户的 头像，openid, 昵称
    '''
    access_token = yield find_access_token()
    if access_token is None:
        raise Return(False)

    client = AsyncHTTPClient()
    resp = yield client.fetch(tornado_options.get_user_list_url.format(access_token, ''))
    openids = json.loads(resp.body).get('data').get('openid')

    result = dict()
    for openid in openids:
        ret = yield get_user_detail(openid)
        tmp = dict(headimgurl = ret.get('headimgurl'), openid = ret.get('openid'), nickname = ret.get('nickname'))
        result[openid] = tmp

    raise Return(result)

@coroutine
def get_user_detail(openid):
    '''
    原样的返回微信返回的信息
    '''
    access_token = yield find_access_token()
    if access_token is None:
        raise Return(False)

    client = AsyncHTTPClient()
    resp = yield client.fetch(tornado_options.get_user_detail_url.format(access_token, openid))
    data = json.loads(resp.body)

    raise Return(data)