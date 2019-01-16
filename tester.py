
from setting import *
from db import RedisClient
import requests
from requests.exceptions import RequestException
import time
class Tester():
    """
    验证代理
    """
    def __init__(self):
        self.redis = RedisClient()

    def test_single_proxy(self,proxy):
        """
        测试单个代理
        """
        try:
            response = requests.get(url=TEST_URL, timeout=5)
            if response.status_code in VALID_STATUS_CODES:
                self.redis.max(proxy) #测试成功 将代理分数设置到最大
                print('测试成功', proxy, time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time())))
            else:
                #print('代理测试失败',proxy, response.status_code)
                self.redis.decrease(proxy)
        except RequestException:
            print('代理测试请求异常', proxy)
            self.redis.decrease(proxy)

    def run(self):
        print('测试器开始 测试代理%d个' % self.redis.count(), time.strftime('%Y-%m-%d %H-%M',time.localtime(time.time())))
        # 从数据库获取全部
        proxies = self.redis.all()
        for proxy in proxies:
            self.test_single_proxy(proxy)








# import asyncio
# import aiohttp
# try:
#     from aiohttp import ClientError
# except:
#     from aiohttp import ClientProxyConnectionError as ProxyConnectionError
# from db import RedisClient
# from setting import *
#
# class Tester():
#     def __init__(self):
#         self.redis = RedisClient()
#
#     async def test_single_proxy(self, proxy):
#         """
#         测试单个代理
#         :return:
#         """
#         conn = aiohttp.TCPConnector(verify_ssl=False)
#         async with aiohttp.ClientSession(connector=conn) as session:
#             try:
#                 if isinstance(proxy,bytes):
#                     proxy = proxy.decode('utf-8')
#                 real_proxy = 'http://' + proxy
#                 async with session.get(TEST_URL, proxy=real_proxy, timeout=15, allow_redirects=False) as response:
#                     if response.status in VALID_STATUS_CODES:
#                         self.redis.max(proxy)
#                         print('代理可用', proxy)
#                     else:
#                         self.redis.decrease(proxy)
#                         print('请求响应码不合法', response.status, proxy)
#             except(ClientError, aiohttp.client_exceptions.ClientConnectionError, asyncio.TimeoutError, AttributeError):
#                 self.redis.decrease(proxy)
#                 print('代理请求失败', proxy)
#
#     def run(self):
#         """
#         测试主函数
#         :return:
#         """
#         print('测试器开始运行')
#         try:
#             count = self.redis.count()
#             print('当前剩余', count, '个代理')
#             for i in range(0, count, BATCH_TEST_SIZE):
#                 start = i
#                 stop = min(i + BATCH_TEST_SIZE, count)
#                 print('正在测试第', start + 1, '-', stop, '个代理')
#                 test_proxies = self.redis.batch(start, stop)
#                 loop = asyncio.get_event_loop()
#                 tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
#                 loop.run_until_complete(asyncio.wait(tasks))
#                 sys.stdout.flush()
#                 time.sleep(5)
#         except Exception as e:
#             print('测试器发生错误', e.args)
#
#
if __name__ == '__main__':
    Tester().run()
