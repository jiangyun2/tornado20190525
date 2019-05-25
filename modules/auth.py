#!/usr/bin/python
# -*- coding: utf-8 -*


from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from modules.db import Base

from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(50))
    creatime = Column(DateTime, default=datetime.now)
    email = Column(String(80))

    def __repr__(self):
        return "<User:#{}-{}".format(self.id,self.username)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(200))
    thumb_url = Column(String(200))
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User',backref='posts',uselist=False,cascade='all')

    def __repr__(self):
        return "<Post:#{}".format(self.id)

if __name__ == '__main__':
    # 把创建好的Module映射到数据库中
    Base.metadata.create_all()