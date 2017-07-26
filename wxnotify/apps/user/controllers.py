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
#                        2017/7/21  下午4:01

from wxnotify.apps.user import services
from wxnotify.common.route import route
from wxnotify.common import controller
from tornado.gen import coroutine

@route('/api/user/name')
class UserController(controller.APIBaseController):

    @coroutine
    def get(self):
        try:
            user_name = self.get_argument('user_name')

            data = yield services.get_user_info(user_name)

            self.reply(dict(code=0, data=data))

        except Exception as e:
            self.reply(dict(code=500, data=data))


@route('/api/user/list')
class UserListController(controller.APIBaseController):

    @coroutine
    def get(self):
        try:
            data = yield services.get_user_list()

            self.reply(dict(code=0, openids=data))

        except Exception as e:
            self.reply(dict(code=500, data=data))

@route('/api/user/detail')
class UserDetailController(controller.APIBaseController):

    @coroutine
    def get(self):
        try:
            openid = self.get_argument('openid')
            data = yield services.get_user_detail(openid)

            self.reply(dict(code=0, openids=data))

        except Exception as e:
            self.reply(dict(code=500, data=data))
