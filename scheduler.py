# -*- coding: utf-8 -*-
from getter import Getter
from tester import Tester
from setting import *
import time
from multiprocessing import Process
from api import app
class Scheduler():
    def schedule_getter(self):
        getter = Getter()
        while GETTER_ENABLED:
            try:
                getter.run()
            except:
                getter.run()
            time.sleep(GETTER_CYLE)


    def schedule_tester(self):
        tester = Tester()
        while TESTER_ENABLED:
            try:
                tester.run()
            except:
                 tester.run()
            time.sleep(TESTER_CYCLE)

    def schedule_api(self):
        print('开启API')
        app.run(API_HOST,API_PORT)


    def run(self):
        print('代理池开始运行')
        tester_process = Process(target=self.schedule_tester)
        tester_process.start()

        getter_process = Process(target=self.schedule_getter)
        getter_process.start()


        api_process = Process(target=self.schedule_api())
        api_process.start()



