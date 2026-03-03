#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：为 gen_table_column 表添加扩展字段
支持关联表配置、页签配置等功能
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'ruoyi-fastapi-backend'))

from sqlalchemy import create_engine, text
from config.env import DataBaseConfig


def get_database_url():
    """获取数据库连接URL"""
    # DataBaseConfig 是数据库配置实例
    config = DataBaseConfig
    
    if config.db_type == 'mysql':
        return f"mysql+pymysql://{config.db_username}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_database}?charset=utf8mb4"
    elif config.db_type == 'postgresql':
        return f"postgresql+psycopg2://{config.db_username}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_database}"
    else:
        raise ValueError(f"不支持的数据库类型: {config.db_type}")


def migrate_mysql(engine):
    """MySQL 数据库迁移"""
    print("开始执行 MySQL 数据库迁移...")
    
    with engine.connect() as conn:
        # 检查字段是否已存在
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'gen_table_column' 
            AND COLUMN_NAME = 'link_table'
        """))
        
        if result.fetchone()[0] > 0:
            print("字段已存在，跳过迁移")
            return
        
        # 执行迁移
        sqls = [
            "ALTER TABLE `gen_table_column` ADD COLUMN `link_table` VARCHAR(200) NULL COMMENT '关联表名称' AFTER `dict_type`",
            "ALTER TABLE `gen_table_column` ADD COLUMN `link_label_field` VARCHAR(200) NULL COMMENT '关联表标签字段' AFTER `link_table`",
            "ALTER TABLE `gen_table_column` ADD COLUMN `link_value_field` VARCHAR(200) NULL COMMENT '关联表值字段' AFTER `link_label_field`",
            "ALTER TABLE `gen_table_column` ADD COLUMN `tab_page` VARCHAR(50) NULL DEFAULT 'basic' COMMENT '显示页签（basic基本信息/detail详细信息）' AFTER `link_value_field`",
            "ALTER TABLE `gen_table_column` ADD COLUMN `default_value` VARCHAR(500) NULL COMMENT '默认值' AFTER `tab_page`",
            "ALTER TABLE `gen_table_column` ADD COLUMN `example_value` VARCHAR(500) NULL COMMENT '示例值' AFTER `default_value`",
            "ALTER TABLE `gen_table_column` ADD COLUMN `list_width` INT NULL COMMENT '列表显示宽度（像素）' AFTER `example_value`",
        ]
        
        for sql in sqls:
            try:
                conn.execute(text(sql))
                print(f"✓ 执行成功: {sql[:50]}...")
            except Exception as e:
                print(f"✗ 执行失败: {sql[:50]}...")
                print(f"  错误信息: {e}")
        
        conn.commit()
    
    print("MySQL 数据库迁移完成！")


def migrate_postgresql(engine):
    """PostgreSQL 数据库迁移"""
    print("开始执行 PostgreSQL 数据库迁移...")
    
    with engine.connect() as conn:
        # 检查字段是否已存在
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM information_schema.columns 
            WHERE table_name = 'gen_table_column' 
            AND column_name = 'link_table'
        """))
        
        if result.fetchone()[0] > 0:
            print("字段已存在，跳过迁移")
            return
        
        # 执行迁移
        sqls = [
            ("ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS link_table VARCHAR(200) NULL", 
             "COMMENT ON COLUMN gen_table_column.link_table IS '关联表名称'"),
            ("ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS link_label_field VARCHAR(200) NULL",
             "COMMENT ON COLUMN gen_table_column.link_label_field IS '关联表标签字段'"),
            ("ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS link_value_field VARCHAR(200) NULL",
             "COMMENT ON COLUMN gen_table_column.link_value_field IS '关联表值字段'"),
            ("ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS tab_page VARCHAR(50) NULL DEFAULT 'basic'",
             "COMMENT ON COLUMN gen_table_column.tab_page IS '显示页签（basic基本信息/detail详细信息）'"),
            ("ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS default_value VARCHAR(500) NULL",
             "COMMENT ON COLUMN gen_table_column.default_value IS '默认值'"),
            ("ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS example_value VARCHAR(500) NULL",
             "COMMENT ON COLUMN gen_table_column.example_value IS '示例值'"),
            ("ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS list_width INT NULL",
             "COMMENT ON COLUMN gen_table_column.list_width IS '列表显示宽度（像素）'"),
        ]
        
        for add_sql, comment_sql in sqls:
            try:
                conn.execute(text(add_sql))
                conn.execute(text(comment_sql))
                print(f"✓ 执行成功: {add_sql[:50]}...")
            except Exception as e:
                print(f"✗ 执行失败: {add_sql[:50]}...")
                print(f"  错误信息: {e}")
        
        conn.commit()
    
    print("PostgreSQL 数据库迁移完成！")


def main():
    """主函数"""
    try:
        # 获取数据库连接
        database_url = get_database_url()
        engine = create_engine(database_url, echo=False)
        
        # 获取数据库类型
        config = DataBaseConfig
        
        print(f"数据库类型: {config.db_type}")
        print(f"数据库地址: {config.db_host}:{config.db_port}/{config.db_database}")
        print("-" * 60)
        
        # 根据数据库类型执行迁移
        if config.db_type == 'mysql':
            migrate_mysql(engine)
        elif config.db_type == 'postgresql':
            migrate_postgresql(engine)
        else:
            print(f"不支持的数据库类型: {config.db_type}")
            return
        
        print("-" * 60)
        print("迁移完成！")
        
    except Exception as e:
        print(f"迁移失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
