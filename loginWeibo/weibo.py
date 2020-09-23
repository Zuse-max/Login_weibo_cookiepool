#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import urllib
import base64
import re
import time
from .utils import WbUtils

sso_login = 'ssologin.js(v1.4.19)'

class WeiboLogin(object):
    def __init__(self, account, password):
        self.account = account
        self.password = password
        #用户ID
        self.uid=''

        # 建立新的会话
        self.session = requests.session()
        # 设置请求头
        self.session.headers = {
            'Referer':'https://mail.sina.com.cn/?from=mail',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        }
        
        self.prelogin_url='https://login.sina.com.cn/sso/prelogin.php'
        self.login_url='https://login.sina.com.cn/sso/login.php?client=%s'

    def login_mail(self):
        """
        用用户名和密码，登录新浪邮箱
        :return:uid：用户ID
        """
        # 1.PreLogin
        #request.su=sinaSS0Encode.base64.encode(urlencode(username)) 对用户名进行加密
        su = base64.b64encode(urllib.parse.quote(self.account).encode('utf-8')).decode('utf-8')
        params={
            "entry":"cnmail",
            "callback":"sinaSSOController.preloginCallBack",
            "su":su,#base64编码之后的用户账号
            "rsakt":"mod",
            "client":"ssologin.js(v1.4.19)",
            "_":int(time.time()*1000)#时间戳
            }
        headers={
            'Referer':'https://mail.sina.com.cn/?from=mail',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
            'Cache-Control':'max-age=0',
            'Accept':'*/*',
            'Accept-Language':'zh-Hans-CN,zh-Hans;q=0.5',
            'Accept-Encoding':'gzip, deflate, br',
            'Host':'login.sina.com.cn',
            'Connection':'Keep-Alive'
            }
        resp = self.session.get(self.prelogin_url,params=params,headers=headers,verify = False)
        pre_login = json.loads(re.match(r'[^{]+({.+?})', resp.text).group(1))

        # 2.Login
        resp = self.session.post(self.login_url  % sso_login, 
                                 data=WbUtils.getLoginStructure(self.account, self.password, pre_login),
                                 verify = False)
        resp.encoding='gbk'
        
        # 3.CrossDomain
        crossdomain2 = re.search(r'(https://[^;]*)', resp.text).group(1)
        #print('crossdomain2',crossdomain2)
        resp = self.session.get(crossdomain2,verify = False)
       
        # 4.Passport
        passporturl = re.search('(https://passport[^\"]*)', resp.text.replace('\/', '/')).group(0)
        #print('passporturl ',passporturl)
        resp = self.session.get(passporturl,verify = False)
        resp.encoding='gbk'
        
        # 获取登录信息
        login_info = json.loads(re.search('\((\{.*\})\)', resp.text).group(1))
        uid = login_info["userinfo"]["uniqueid"]
        self.uid = uid
        #print("新浪邮箱登陆成功。","用户id为",uid)
        return(uid)

    def login_weibo(self):
        """
        登录微博,获取并保存uid
        :return：response
        """
        self.session.headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
            }
        uid = self.login_mail()
        
        resp = self.session.get('https://weibo.com/u/%s/home?wvr=5' % uid)
        #nick = re.search(r"\$CONFIG\['nick']='(.*?)';",resp.text).group(1)
        #print('登陆成功,','微博用户名为',nick)
        return resp
         
    def getcookies(self):
        """"
        返回登录微博后的cookies
        :return：cookies
        """
        resp = self.login_weibo()
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        return cookies_dict
    
    def get_uid(self):
        return self.uid

if __name__ == "__main__":
    login=WeiboLogin()
    login.login_weibo
