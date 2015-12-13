#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class Episode(object):

  def __init__(self, url=None, post=None, title=None):
    self.url = url
    self.post = post
    
    self.title = title
    self.images = None
    self.timestamp = None

  def get_params(self):
    params = {
      't' : self.title,
    }
    return params

  def to_json(self):
    data = {
      't' : self.title,
      'ts' : self.timestamp,
    }

    images = []
    for image in self.images:
      if not image.name:
        continue
      images.append(image.name)

    data['i'] = images

    if self.post.image:
      data['c'] = self.post.image.name
  
    return json.dumps(data)

  def test(self):
    print self.title, self.images
