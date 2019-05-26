#!/usr/bin/python
# -*- coding: utf-8 -*

import uuid
import tornado.web
import tornado.escape
import tornado.websocket
from handlers.main import BaseHandler


class RoomHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        chat = {
            'id': 1234,
            'username': self.current_user,
            'body': "message1234",
        }
        msg = [
            {
                'html': self.render_string('message.html', chat=chat)
            },
        ]
        self.render("room.html",user=self.current_user, messages=msg)



class EchoWebSocket(tornado.websocket.WebSocketHandler):
    # 用户集合
    waituser = set()

    def open(self):
        EchoWebSocket.waituser.add(self)
        print("WebSocket opened")
        print(EchoWebSocket.waituser)

    def on_message(self, message):
        print("got messages:{}".format(message))
        parsed = tornado.escape.json_decode(message)
        msg = parsed['body']
        user = parsed['user']
        chat = {
            'id': str(uuid.uuid4()),
            'body': msg,
            'username': user,
        }
        chat['html'] = tornado.escape.to_basestring(self.render_string('message.html', chat=chat))
        for w in EchoWebSocket.waituser:
            w.write_message(chat)

    def on_close(self):
        EchoWebSocket.waituser.remove(self)
        print("WebSocket closed")




















