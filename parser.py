#!/usr/bin/pythonA
# -*- coding: utf-8 -*-

import os
import urllib
import urlparse
import time

import raven
import requests
import BeautifulSoup

import post
import episode
import attachment

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'

class PostListParser(object):

  def __init__(self, url=None):
    self.url = url
    
    self.hostname = urlparse.urlparse(url=self.url).hostname
    self.session = requests.Session()
    self.headers = {
      'User-Agent': USER_AGENT,
      'Referer': self.url
    }

  def parse(self):
    response = self._get_response()
    response.encoding = 'utf-8'
    if not response.status_code / 100 == 2:
      return []
  
    doc = BeautifulSoup.BeautifulSoup(response.text)

    urls = {}
    posts = []

    for e in doc.findAll('a'):

      c = e.get('class')
      href = e.get('href', None)
      title = e.text.strip()


      if not c:
        continue

      if not title:
        continue

      if not href:
        continue

      if not 'page_id' in href:
        continue

      if '(' == title[0]:
        continue

      urls[href] = True

    for url in urls.keys():
      p = post.Post(title=None, url=url, image=None)
      posts.append(p)

    return posts

  def _get_response(self, url=None):
    if not url:
      url = self.url
    return self.session.get(url, headers=self.headers)
  
class PostParser(object):

  def __init__(self, session=None, post=None):
    self.session = session
    self.post = post

    self.hostname = urlparse.urlparse(url=self.post.url).hostname
    self.headers = {
      'User-Agent': USER_AGENT,
      'Referer': self.post.url
    }

  def parse(self):
    response = self._get_response(self.post.url)
    response.encoding = 'utf-8'
    if not response.status_code / 100 == 2:
      return self.post

    doc = BeautifulSoup.BeautifulSoup(response.text)
    episodes = []

    for e in doc.findAll('p'):
      a = e.find('a')

      if not a:
        continue

      href = a.get('href',None)

      title = str(unicode(a.text.strip()))
      if not title :
        continue

      ep = episode.Episode(url=href, post=self.post, title=title)
      episodes.append(ep)

    return episodes

  def _get_response(self, url=None):
    return self.session.get(url, headers=self.headers)

class EpisodeParser(object):

  def __init__(self, session=None, episode=None, referer=None):
    self.session = session
    self.episode = episode
    self.headers = {
      'User-Agent': USER_AGENT,
      'Referer': referer
    }

  def parse(self):

    response = self._get_response(self.episode.url)
    response.encoding = 'utf-8'
    if not response.status_code / 100 == 2:
      return self.episode

    doc = BeautifulSoup.BeautifulSoup(response.text)
    images = []

    for img in doc.findAll('img'):
      src = img.get('src',None)

      if not '.jpg' in src and not '.JPG' in src:
        continue

      r = requests.get(src)
      if not r.status_code / 100 == 2 or not r.content:
        continue

      i = attachment.Image(name=src, content=r.content)
      images.append(i)

    self.episode.images = images
    
    return self.episode
  
  def _get_response(self, url=None):
    return self.session.get(url, headers=self.headers)
