# -*- coding: utf-8 -*-
from Generator import WeiboCookiesGenerator
from tester import WeiboValidTester

def main():
    WeiboCookiesGenerator().run()
    WeiboValidTester().run()

if __name__ == '__main__':
    main()

