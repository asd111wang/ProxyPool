# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from scheduler import Scheduler
from setting import *
import sys
import time

def main():
    try:
        scheduler = Scheduler()
        scheduler.run()
    except:
        main()
        # print('爬虫异常退出', time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))
        # sys.exit()

if __name__ == '__main__':
   main()
