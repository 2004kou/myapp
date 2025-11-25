from flask import g,request
import pymysql
from pymysqlpool.pool import Pool, TimeoutError
import os
import logging



class DB:
    @classmethod
    def init_pool(cls):
        pool = Pool(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
            max_size=100,
           # 文字コード
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        pool.init()
        return pool
    
