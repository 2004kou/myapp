from flask import g,request
import pymysql
from pymysqlpool.pool import Pool
import os



class DB:
    @classmethod
    def init_pool(cls):
        pool = Pool(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
            max_size=20,
           # 文字コード
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        pool.init()
        return pool
    
db_use = DB.init_pool()
    

def before_request():
    if request.endpoint and request.endpoint.startswith('static'):
        print("before_request: static file, no DB connection")
        return
    try:
        g.db_conn = db_use.get_conn()
        g.db_cursor = g.db_conn.cursor()
        print("before_request: connection opened")
    except Exception as e:
        print(f"before_request: failed to open connection: {e}")


def teardown_request(exception):
    db_conn = getattr(g, "db_conn", None)
    if db_conn is not None:
        db_conn.close()
        print("teardown_request: connection closed")


def ensure_conn():
    db_cursor = getattr(g, "db_cursor", None)
    if db_cursor is None:
        # 接続がまだない場合は新しく作る
        g.db_conn = db_use.get_conn()
        g.db_cursor = g.db_conn.cursor()
        print("ensure_conn: new connection created")
        return
    try:
        db_cursor.execute("SELECT 1")
        print("ensure_conn: connection alive")
    except (pymysql.err.InterfaceError, pymysql.err.OperationalError):
        print("ensure_conn: reconnecting...")
        g.db_conn = db_use.get_conn()
        g.db_cursor = g.db_conn.cursor()


