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

from wxnotify.apps.message import services
from wxnotify.common.route import route
from wxnotify.common import controller
from tornado.gen import coroutine
import xmltodict

@route('/api/wechat/msg')
class MessageController(controller.APIBaseController):

    @coroutine
    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')

            code = yield services.check_signature(signature, timestamp, nonce, echostr)

            if code != None:
                self.finish(code)

        except Exception as e:
            self.reply(dict(code=500, msg='check signature error'))

    @coroutine
    def post(self):
        try:
            request_dict = xmltodict.parse(self.request.body).get('xml')

            MsgType = request_dict.get('MsgType')
            Content = request_dict.get('Content')
            FromUserName = request_dict.get('FromUserName')
            ToUserName = request_dict.get('ToUserName')
            MsgId = request_dict.get('MsgId')
            CreateTime = request_dict.get('CreateTime')

            if MsgType != 'text':
                self.reply(dict(code=4003, msg='MsgType must is text'))

            if Content.startswith('bind:'):
                user_name = Content.strip('bind:')
                data = yield services.user_bind(user_name, FromUserName)

            self.reply(dict(code=0, data=data))

        except Exception as e:
            self.reply(dict(code=500, msg='error'))