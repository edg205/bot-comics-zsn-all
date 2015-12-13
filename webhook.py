#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import requests

class Webhook(object):

  def __init__(self, webhook_url, s3_url):
    self.webhook_url = webhook_url
    self.s3_url = s3_url
    self.collection = self.webhook_url.split('/')[-1]

  def exist(self, episode):
    params = episode.get_params()
    r = requests.get(self.webhook_url, params=params)

    if not r.content:
      print 'not found', episode.title
      return False

    print 'found', episode.title
    return True

  def send(self, episode):
    ts = str(int(time.time() * 1000))
    episode.timestamp = ts

    if episode.post.image:
      self._upload(ts, episode.post.image)

    for image in episode.images:
      self._upload(ts, image)
    
    data = episode.to_json()
    requests.post(self.webhook_url, data=data)
  
  def _upload(self, ts, attachment):
    headers = {
      'Content-Type': 'application/octet-stream'
    }

    params = {
      'name': self.collection + '/' + ts + '/' + attachment.name
    }

    r = requests.put(self.s3_url, params=params, data=attachment.content, headers=headers)
    print params, r.status_code
    
    if not r.status_code / 100 == 2:
      return False
    return True
    
