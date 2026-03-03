-- 为 gen_table_column 表添加扩展字段（PostgreSQL 版本）
-- 用于支持关联表配置、页签配置等功能

-- 添加关联表字段
ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS link_table VARCHAR(200) NULL;
COMMENT ON COLUMN gen_table_column.link_table IS '关联表名称';

-- 添加关联表标签字段
ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS link_label_field VARCHAR(200) NULL;
COMMENT ON COLUMN gen_table_column.link_label_field IS '关联表标签字段';

-- 添加关联表值字段
ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS link_value_field VARCHAR(200) NULL;
COMMENT ON COLUMN gen_table_column.link_value_field IS '关联表值字段';

-- 添加页签配置字段
ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS tab_page VARCHAR(50) NULL DEFAULT 'basic';
COMMENT ON COLUMN gen_table_column.tab_page IS '显示页签（basic基本信息/detail详细信息）';

-- 添加默认值字段
ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS default_value VARCHAR(500) NULL;
COMMENT ON COLUMN gen_table_column.default_value IS '默认值';

-- 添加示例值字段
ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS example_value VARCHAR(500) NULL;
COMMENT ON COLUMN gen_table_column.example_value IS '示例值';

-- 添加列表宽度字段
ALTER TABLE gen_table_column ADD COLUMN IF NOT EXISTS list_width INT NULL;
COMMENT ON COLUMN gen_table_column.list_width IS '列表显示宽度（像素）';
