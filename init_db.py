import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 连接配置
DB_HOST = '127.0.0.1'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = '375529'
DB_NAME = 'ruoyi-fastapi'
SQL_FILE = 'ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg.sql'

try:
    # 连接到PostgreSQL服务器（连接到默认的postgres数据库）
    print("正在连接到PostgreSQL服务器...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database='postgres'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # 检查数据库是否存在
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cursor.fetchone()
    
    if exists:
        print(f"数据库 {DB_NAME} 已存在，跳过创建")
    else:
        # 创建数据库
        print(f"正在创建数据库 {DB_NAME}...")
        cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
        print(f"数据库 {DB_NAME} 创建成功！")
    
    cursor.close()
    conn.close()
    
    # 连接到新创建的数据库并执行SQL文件
    print(f"正在连接到数据库 {DB_NAME}...")
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    # 读取并执行SQL文件
    print(f"正在执行SQL文件 {SQL_FILE}...")
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    cursor.execute(sql_content)
    conn.commit()
    
    print("SQL文件执行成功！")
    print("数据库初始化完成！")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
