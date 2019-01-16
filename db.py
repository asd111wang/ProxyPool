# -*- coding: utf-8 -*-
import redis
import re
from setting import *
from random import choice
from error import PoolEmptyError


class RedisClient():
    def __init__(self,host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化Redis数据库
        :param host: 主机地址
        :param port: 端口
        :param password: Redis数据库密码
        :return:
        """
        #加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型。
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理到Redis数据库，设置分数为最高
        :param proxy:代理
        :param score:分数
        :return:添加结果
        """
        # 1、检查代理是否符合规范
        if not re.match('\d+\.\d+\.\d+\.\d+:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        # 2、获取代理对应的分数，如果有说明存在此代理，不做添加操作，反之
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
        随机获取有效代理，最高分数代理优先，如果不存在，按照排名获取否则异常
        :return:随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)  #从大到小排序
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return:修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        print(score)
        if score and score > MIN_SCORE:
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('代理',proxy,'当前分数',score,'移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy:代理
        :return:是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return:设置结果
        """
        #print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取代理数量
        :return:数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return:
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self,start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return:代理列表
        """
        return self.db.zrevrange(REDIS_KEY,start, stop-1)


if __name__ == '__main__':
    con =RedisClient()
    print(con.batch(0,100))