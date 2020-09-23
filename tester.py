# -*- coding: utf-8 -*-
import json
import requests
from requests.exceptions import ConnectionError
from RedisClient import RedisClient
from settings import *

class WeiboValidTester(object):
    def __init__(self, website='weibo'):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.uid_db = RedisClient('uid',self.website)
    
    def test(self, username, cookies):
        print('正在测试Cookies', '用户名', username)
        try:
            cookies = json.loads(cookies)
        except TypeError:
            print('Cookies不合法', username)
            self.cookies_db.delete(username)
            print('删除Cookies', username)
            return
        try:
            test_url = TEST_URL_MAP[self.website]
            response = requests.get(test_url % self.uid_db.get(username), cookies=cookies, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                print('Cookies有效', username)
            else:
                print(response.status_code, response.headers)
                print('Cookies失效', username)
                self.cookies_db.delete(username)
                print('删除Cookies', username)
        except ConnectionError as e:
            print('发生异常', e.args)
        
    def run(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            self.test(username, cookies)

if __name__ == '__main__':
    WeiboValidTester().run()