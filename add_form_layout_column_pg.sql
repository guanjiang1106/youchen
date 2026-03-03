-- 为 gen_table 表添加 form_layout 字段（PostgreSQL 版本）
-- 用于存储表单布局配置（JSON格式）

-- 添加字段
ALTER TABLE gen_table ADD COLUMN IF NOT EXISTS form_layout VARCHAR(5000) NULL;

-- 添加字段注释
COMMENT ON COLUMN gen_table.form_layout IS '表单布局配置（JSON格式）';
