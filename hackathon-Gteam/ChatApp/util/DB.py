from flask import g,request
import pymysql
from pymysqlpool.pool import Pool, TimeoutError
import os



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
    
db_use = DB.init_pool()
    

def get_conn_with_retry(retries=3):
    for i in range(retries):
        try:
            return db_use.get_conn()
        except TimeoutError as e:
            print(f"get_conn retry {i+1}/{retries} failed: {e}")
    raise KTimeoutError("All retries failed")

# --- リクエスト開始時 ---
def before_request():
    if request.endpoint and request.endpoint.startswith('static'):
        print("before_request: static file, no DB connection")
        return
    try:
        g.db_conn = get_conn_with_retry()
        g.db_cursor = g.db_conn.cursor()
        print("before_request: connection opened")
    except Exception as e:
        print(f"before_request: failed to open connection: {e}")

# --- リクエスト終了時 ---
def teardown_request(exception):
    db_conn = getattr(g, "db_conn", None)
    if db_conn is not None:
        try:
            db_conn.close()
            print("teardown_request: connection closed")
        except Exception as e:
            print(f"teardown_request: error closing connection: {e}")
    else:
        print("teardown_request: no connection to close")

# --- 接続確認・再接続 ---
def ensure_conn():
    db_cursor = getattr(g, "db_cursor", None)
    if db_cursor is None:
        g.db_conn = get_conn_with_retry()
        g.db_cursor = g.db_conn.cursor()
        print("ensure_conn: new connection created")
        return
    try:
        db_cursor.execute("SELECT 1")
        print("ensure_conn: connection alive")
    except (pymysql.err.InterfaceError, pymysql.err.OperationalError):
        print("ensure_conn: reconnecting...")
        g.db_conn = get_conn_with_retry()
        g.db_cursor = g.db_conn.cursor()

