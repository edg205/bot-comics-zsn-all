#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import random

class Image(object):

  def __init__(self, name=None, content=None):
    if '?' in name:
      name = name.split('?')[0]
      
    self.content = content
    self.extension = name.split('.')[-1]
    self.name = self.id_generator() + '.' + self.extension
    
  def id_generator(self, size=24, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
