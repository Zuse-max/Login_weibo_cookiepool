#!/usr/bin/python
# -*- coding: utf-8 -*-
# 测试脚本

from weibo import WeiboLogin

if __name__ == '__main__':
    we = WeiboLogin('zfhuaping@sina.com', 'a951687423@')
    we.login_weibo
