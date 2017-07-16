import os
import time
import requests
import random
from slackclient import SlackClient
from pyquery import PyQuery

if __name__ == "__main__":
    pre_url = 'http://www.guru3d.com/'
    url = 'http://www.guru3d.com/files-categories/videocards-nvidia-geforce-vista-%7C-7.html'
    headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0"}
    forum_page = requests.get(url, headers=headers).content
    pq = PyQuery(forum_page)
    first_post_title = pq("h1")[0]
    driver_version = first_post_title.text_content().split('driver')[0].strip()
    page_url = pre_url + first_post_title.getnext().getnext().find('a').get('href')
