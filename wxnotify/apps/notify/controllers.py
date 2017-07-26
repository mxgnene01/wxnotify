# -*- coding: utf-8 -*-
#
from wxnotify.apps.notify import services
import wxnotify.apps.user.services as user_services
from wxnotify.common.route import route
from wxnotify.common import controller
from tornado.gen import coroutine
import datetime
import json

@route('/api/wechat/get_access_token')
class AccessTokenController(controller.APIBaseController):

    @coroutine
    def get(self):
        access_token = yield services.find_access_token()

        self.reply(dict(code=0, token=access_token))


@route('/api/push/byopenid')
class OpenidNotifySendController(controller.APIBaseController):

    @coroutine
    def get(self, openid):
        openid = self.get_argument('openid')
        title = self.get_argument('title')
        time = self.get_argument('time', str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        machine = self.get_argument('machine')
        moniterkey = self.get_argument('moniterkey')
        state = self.get_argument('state')
        output = self.get_argument('output')
        remark = self.get_argument('remark')
        url = self.get_argument('url', 'touch.daling.com')

        code, ret = yield services.send_notify(openid, title, time, machine, moniterkey, state, output, remark, url )
        if not code:
            self.reply(dict(code=5003,
                            reason="can't push notify"))
            return

        self.reply(dict(code=0, original=json.loads(ret)))

@route('/api/push/byusername')
class UserNotifySendController(controller.APIBaseController):

    @coroutine
    def get(self):
        user_names = self.get_argument('user_names')
        title = self.get_argument('title')
        time = self.get_argument('time', str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        machine = self.get_argument('machine')
        moniterkey = self.get_argument('moniterkey')
        state = self.get_argument('state')
        output = self.get_argument('output')
        remark = self.get_argument('remark')
        url = self.get_argument('url', 'touch.daling.com')

        sec = 0

        for user_name in user_names.split(','):
            data = yield user_services.get_user_info(user_name)
            openid = data[0].get('openid')
            code, ret = yield services.send_notify(openid, title, time, machine, moniterkey, state, output, remark, url )
            if code:
                sec = sec + 1


        if len(user_names.split(',')) != sec:
            self.reply(dict(code=5003,
                            reason="push notify hash error"))
            return
        else:
            self.reply(dict(code=0, original=json.loads(ret)))
