#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class Post(object):
   
  def __init__(self, title=None, url=None, image=None):
    self.title = title
    self.url = url
    self.image = None
