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

from tornado.gen import coroutine, Return
from tornado.options import (options as tornado_options,
                             define as tornado_define)
from wxnotify.common.postgres import with_postgres
import logging
import hashlib
import time

tornado_define("token", default='', help="gong zhong hao token", type=str)

BIZLOG = logging.getLogger("wxnotify.business")


@coroutine
def get_msg():
    raise Return(True)


@coroutine
def check_signature(signature, timestamp, nonce, echostr):
    '''
    微信检查服务
    '''

    # 第1步：将token、timestamp、nonce三个参数进行字典序排序
    mylist = sorted([tornado_options.token, timestamp, nonce])  # 将token, timestamp和nonce组成一个列表，然后进行排序

    # 第2步：将三个参数字符串拼接成一个字符串进行sha1加密
    mystr = ''.join(mylist)
    mystr_encoded = hashlib.sha1(mystr).hexdigest()  # 对拼接字符串进行sha1加密

    # 第3步：开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if mystr_encoded == signature:
        raise Return(echostr)
    else:
        raise Return(None)


@coroutine
@with_postgres('master')
def user_bind(db, user_name, openid):
    _now = int(time.time())
    sql = "INSERT INTO dl_user_weixin (user_name, openid, ctime, utime) VALUES ('%s', '%s', %s, %s);" % (user_name, openid, _now, _now)
    try:
        cursor = yield db.execute(sql)

        if cursor.rowcount == 0:
            BIZLOG.error('SAVE WXNOTIFY ERROR: [user_name: %s, openid: %s]' % (user_name, openid))
            raise Return(False)
        else:
            BIZLOG.info('SAVE WXNOTIFY SUCCESS: [user_name: %s, openid: %s, ctime and utime: %s]' % (user_name, openid, _now))
            raise Return(True)
    except Exception, e:
        BIZLOG.error('error info is : %s' % e.message)
        raise Return(False)