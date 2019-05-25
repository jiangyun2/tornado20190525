#!/usr/bin/python
# -*- coding: utf-8 -*

from modules.auth import User, Post
from sqlalchemy import exists

class Sqloperation(object):

    def __init__(self,db_session):
        self.db_session = db_session

    def get_all_post(self):
        return self.db_session .query(Post).all()

    def isexists(self,username):
        # 查询满足条件的项目是否存在
        return self.db_session.query(exists().where(User.username == username)).scalar()

    def add_user(self,username,password,email):
        self.db_session.add(User(username=username, password=password, email=email))
        self.db_session.commit()

    def get_user(self,username):
        return self.db_session .query(User).filter(User.username == username).first()

    def get_password(self,username):
        return self.get_user(username).password

    def update_passwd(self,username,newpasswd):
        self.db_session.query(User).filter(User.username == username).update({User.password: newpasswd})
        self.db_session.commit()

    def add_post(self,img_url,thumb_url,current_user):
        post = Post(image_url=img_url,
                         thumb_url=thumb_url,
                         user_id= self.get_user(current_user).id,
                         )
        self.db_session.add(post)
        self.db_session.flush()
        self.db_session.commit()
        return post.id

    def get_post(self,post_id):
        return self.db_session .query(Post).filter(Post.id == post_id).first()




