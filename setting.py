# -*- coding: utf-8 -*-

#Redis数据库地址
REDIS_HOST = '127.0.0.1'

#Redis端口
REDIS_PORT = 6379

#Redis密码，没有填None
REDIS_PASSWORD = '123'

REDIS_KEY = 'proxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200,302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 100

# 获取循环周期
GETTER_CYLE = 300

# 测试网站
TEST_URL = 'http://www.baidu.com'

#API配置
API_HOST = '0.0.0.0'
API_PORT = 55555

# 最大批量测试量
BATCH_TEST_SIZE = 10

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True


