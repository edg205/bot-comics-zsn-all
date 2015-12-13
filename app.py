#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import httplib
import threading

import bottle
import raven
import requests

import parser
import webhook

def main():
  urls = os.environ.get('URLS', '')
  webhook_url = os.environ.get('WEBHOOK', '')
  s3_url = os.environ.get('S3', '')
  r = raven.Client(os.environ.get('SENTRY_DSN', ''))

  if not urls:
    return
  
  w = webhook.Webhook(webhook_url, s3_url)
  post_list_parsers = []
  
  for url in urls.split(','):
    post_list_parser = parser.PostListParser(url=url)
    post_list_parsers.append(post_list_parser)

  while True:
    try:
      post_parsers = []
      for post_list_parser in post_list_parsers:
        posts = post_list_parser.parse()
        
        for post in posts:
          post_parser = parser.PostParser(
            session=post_list_parser.session,
            post=post
          )
          episodes = post_parser.parse()
          for episode in episodes:

            if w.exist(episode):
              continue
            
            episode_parser= parser.EpisodeParser(
              session=post_parser.session,
              episode=episode,
              referer=post.url
            )
            episode = episode_parser.parse()

            if not episode:
              continue

            if not episode.title:
              continue

            if len(episode.images) < 1:
              continue

            w.send(episode)

            # end
            time.sleep(1)

    except requests.ConnectionError as e:
      print e
      continue
    except httplib.BadStatusLine as e:
      print e
      continue
    except Exception as e:
      print e
      r.captureException()
      
    time.sleep(15 * 60) # 15 min

@bottle.route('/')
def index():
    return ''
    
if __name__ == '__main__':
  reload(sys)
  sys.setdefaultencoding('utf-8') 
  
  port = os.environ.get('PORT', 8888)
  if port == 8888: # debug
    main()
  else:
    threading.Thread(target=main).start()
    bottle.run(host='0.0.0.0', port=port)
