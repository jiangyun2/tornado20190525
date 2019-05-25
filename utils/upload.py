#!/usr/bin/python
# -*- coding: utf-8 -*

from uuid import uuid4
from io import BytesIO
from PIL import Image
import hashlib

class SavePic(object):
    def __init__(self):
        self.thumb_size = (200,200)
        self.savedir = "statics"

    def hash_passd(self,password):
        return hashlib.md5(password.encode()).hexdigest()

    def get_uuidname(self,pic):
        return uuid4().hex + "." + pic['filename'].split(".")[-1]

    def save_imageurl(self,pic):
        uuid_name = self.get_uuidname(pic)
        with open(self.savedir + "/uploads/{}".format(uuid_name), "wb") as f:
            f.write(pic['body'])
        bf = BytesIO()
        bf.write(pic['body'])
        im = Image.open(bf)
        im.thumbnail(self.thumb_size)
        im.save(self.savedir + "/thumbs/{}x{}_{}".format(self.thumb_size[0],self.thumb_size[1], uuid_name), "PNG")
        return "uploads/{}".format(uuid_name),"thumbs/{}x{}_{}".format(self.thumb_size[0],self.thumb_size[1], uuid_name)