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
            CreateTime = request_dict.get('CreateTime')

            if MsgType != 'text':
                raise

            if Content.startswith('bind:'):
                user_name = Content.strip('bind:')
                code = yield services.user_bind(user_name, FromUserName)

                if code:
                    self.write('''
                               <xml>
                                   <ToUserName><![CDATA[{0}]]></ToUserName>
                                   <FromUserName><![CDATA[{1}]]></FromUserName>
                                   <CreateTime>{2}</CreateTime>
                                   <MsgType><![CDATA[{3}]]></MsgType>
                                   <Content><![CDATA[{4}]]></Content>
                               </xml>
                               '''.format(FromUserName, ToUserName, CreateTime, MsgType, "绑定成功"))
                else:
                    self.write('''
                                <xml>
                                    <ToUserName><![CDATA[{0}]]></ToUserName>
                                    <FromUserName><![CDATA[{1}]]></FromUserName>
                                    <CreateTime>{2}</CreateTime>
                                    <MsgType><![CDATA[{3}]]></MsgType>
                                    <Content><![CDATA[{4}]]></Content>
                                </xml>
                                '''.format(FromUserName, ToUserName, CreateTime, MsgType, "绑定失败，已绑定或绑定失败，请重试一次"))
                    self.finish()
            elif Content == 'unbind':
                code = yield services.unbind(FromUserName)
                self.write('success')
                self.finish()

            else:
                # 直接回复success（推荐方式）, 微信认为接收消息成功
                self.write('success')
                self.finish()

        except Exception as e:
            # 直接回复success（推荐方式）, 微信认为接收消息成功
            self.write('success')
            self.finish()