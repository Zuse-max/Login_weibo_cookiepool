# -*- coding: utf-8 -*-
from settings import *
from RedisClient import RedisClient
from weibocookies import WeiboCookies
import json

class WeiboCookiesGenerator(object):
    def __init__(self, website='weibo'):
        """
        初始化一些对象
        :param website: 名称
        :param browser: 浏览器, 若不使用浏览器则可设置为 None
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
        self.uid_db=RedisClient('uid',self.website)
    
    def run(self):
        """
        运行, 得到所有账户, 然后逐个模拟登录获取cookies,以及uid
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()
        
        for username in accounts_usernames:
            if not username in cookies_usernames:
                password = self.accounts_db.get(username)
                print('正在生成Cookies', '账号', username, '密码', password)
                result = self.new_cookies(username, password)
                # 成功获取
                if result.get('status') == 1:
                    cookies = result.get('content')#cookies为dict类型
                    uid = result.get('uid')
                    print('成功获取到Cookies', cookies,'成功获取到uid',uid)
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('成功保存Cookies')
                    if self.uid_db.set(username, uid):
                        print('成功保存uid')
                # 登录出错
                elif result.get('status') == 0:
                    print(result.get('content'))
        else:
            print('所有账号都已经成功获取Cookies')
 
    def new_cookies(self, username, password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        return WeiboCookies(username, password).main()

if __name__ == '__main__':
    WeiboCookiesGenerator().run()
    