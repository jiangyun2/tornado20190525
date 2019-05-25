#!/usr/bin/python
# -*- coding: utf-8 -*

import tornado.web
from pycket.session import SessionMixin
from utils.sqloperate import Sqloperation
from utils.upload import SavePic
from modules.db import  Session

savepic = SavePic()


class BaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        # return self.get_secure_cookie("mycookie")
        # 使用self.session.get获取cookie值
        return self.session.get("mycookie")

    # 请求之前调用
    def prepare(self):
        self.db_session = Session()
        self.sqloperation = Sqloperation(self.db_session)

    # 请求之后调用
    def on_finish(self):
        self.db_session.close()

class IndexHandler(BaseHandler):
    '''
    首页，用户上传图片的展示
    :return:
    '''

    @tornado.web.authenticated
    def get(self):
        self.render('index.html',post=self.sqloperation.get_all_post(),user=self.current_user)


class SignupHandler(BaseHandler):
    '''
    用户注册
    :return:
    '''
    def get(self):
        self.render('signup.html',user=self.current_user)

    def post(self):
        username = self.get_argument('username', None)
        email = self.get_argument('email', None)
        passwd1 = self.get_argument('passwd1',None)
        passwd2 = self.get_argument('passwd2', None)
        if passwd1!=passwd2:
            self.write("两次密码不相同")
            return
        if self.sqloperation.isexists(username):
            self.write("该用户已经被注册")
            return
        else:
            self.sqloperation.add_user(username,savepic.hash_passd(passwd1),email)
            self.write("注册成功:{}".format(username))

class ChangePHandler(BaseHandler):
    '''
    修改密码
    :return:
    '''
    def get(self):
        self.render('changep.html',user=self.current_user)

    def post(self):
        username = self.get_argument('username', None)
        passwd = self.get_argument('passwd', None)
        newpasswd1 = self.get_argument('newpasswd1', None)
        newpasswd2 = self.get_argument('newpasswd2', None)
        if newpasswd1 != newpasswd2:
            self.write("两次密码不相同")
            return
        if self.sqloperation.get_password(username) == savepic.hash_passd(passwd):
            self.sqloperation.update_passwd(username,savepic.hash_passd(newpasswd1))
            self.write("修改密码成功")
            self.redirect("/exit")
        else:
            self.write("账号或密码错误")
class LoginHandler(BaseHandler):
    '''
    用户登录
    :return:
    '''
    def get(self):
        self.render('login.html',next_url=self.get_argument('next',None),user=self.current_user)

    def post(self, *args, **kwargs):
        username = self.get_argument('username',None)
        passwd = self.get_argument('passwd',None)
        next_url = self.get_argument('next',None)
        if str(next_url) == "None" or str(next_url) == "/exit":
            next_url = "/"
        if not self.sqloperation.isexists(username):
            self.redirect("/login")
            return
        if self.sqloperation.get_password(username) == savepic.hash_passd(passwd):
            self.session.set('mycookie', username)
            # 登录成功，跳转到next_url
            self.redirect(next_url)
        else:
            # 登录失败，继续登录界面
            self.redirect("/login")


class Exit1Handler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write('退出登录！')
        self.session.set('mycookie', None)
        self.redirect("/login")

class UploadHandler(BaseHandler):
    '''
    图片上传
    '''

    @tornado.web.authenticated
    def get(self):
        self.render('upload.html', user=self.current_user)

    def post(self):
        pic = self.request.files.get('picture',[])[0]
        img_url,thumb_url = savepic.save_imageurl(pic)
        post_id = self.sqloperation.add_post(img_url,thumb_url,self.current_user)
        self.redirect("/post/{}".format(post_id))

class ExploreHandler(BaseHandler):
    '''
    最近上传的图片页面
    :return:
    '''
    @tornado.web.authenticated
    def get(self):
        self.render('explore.html',post=self.sqloperation.get_all_post(),user=self.current_user)


class PostHandler(BaseHandler):
    '''
    单个图片详情页面
    :return:
    '''
    @tornado.web.authenticated
    def get(self, post_id):
        self.render('post.html',post=self.sqloperation.get_post(post_id),user=self.current_user)