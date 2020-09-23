# -*- coding: utf-8 -*-
from loginWeibo.weibo import WeiboLogin

class WeiboCookies(object):
    def __init__(self, username, password):
        self.WeiboLogin = WeiboLogin(username,password)
        
    def main(self):
        """
        获取cookies和uid，返回状态码和cookies或者报错信息
        :return:result字典类型
        """
        try:
            cookies = self.WeiboLogin.getcookies()
            uid = self.WeiboLogin.get_uid()
        except:
            return {
                'status': 0,
                'content': '获取cookies失败',
                'uid':None
            }
        else:
            return {
                'status': 1,
                'content': cookies,
                'uid': uid
            }
