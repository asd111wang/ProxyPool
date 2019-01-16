# -*- coding: utf-8 -*-
from flask import Flask,g
from db import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h1>successful</h1>'

@app.route('/get')
def get_proxy():
    """
    获取一个代理
    :return:随机代理
    """
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_counts():
    """
    获取代理个数
    :return:
    """
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()