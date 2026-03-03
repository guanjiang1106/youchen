"""
数据库迁移脚本：添加 form_layout 字段
"""
import asyncio
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent / 'ruoyi-fastapi-backend'))

from sqlalchemy import text
from config.get_db import get_db


async def migrate():
    """执行数据库迁移"""
    print("=" * 50)
    print("开始执行数据库迁移：添加 form_layout 字段")
    print("=" * 50)
    
    try:
        # 获取数据库连接
        async for db in get_db():
            # 检查字段是否已存在
            check_sql = """
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'gen_table' 
                AND column_name = 'form_layout'
            """
            result = await db.execute(text(check_sql))
            exists = result.fetchone()
            
            if exists:
                print("✓ form_layout 字段已存在，无需迁移")
                return
            
            # 添加字段
            print("正在添加 form_layout 字段...")
            alter_sql = """
                ALTER TABLE gen_table 
                ADD COLUMN form_layout VARCHAR(5000) NULL
            """
            await db.execute(text(alter_sql))
            
            # 添加注释
            print("正在添加字段注释...")
            comment_sql = """
                COMMENT ON COLUMN gen_table.form_layout 
                IS '表单布局配置（JSON格式）'
            """
            await db.execute(text(comment_sql))
            
            # 提交事务
            await db.commit()
            
            print("=" * 50)
            print("✓ 迁移成功！")
            print("=" * 50)
            break
            
    except Exception as e:
        print("=" * 50)
        print(f"✗ 迁移失败：{str(e)}")
        print("=" * 50)
        raise


if __name__ == '__main__':
    asyncio.run(migrate())
