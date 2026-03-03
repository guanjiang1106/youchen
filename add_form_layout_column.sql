-- 为 gen_table 表添加 form_layout 字段
-- 用于存储表单布局配置（JSON格式）

-- MySQL 版本
ALTER TABLE `gen_table` ADD COLUMN `form_layout` VARCHAR(5000) NULL COMMENT '表单布局配置（JSON格式）' AFTER `gen_path`;

-- PostgreSQL 版本
-- ALTER TABLE gen_table ADD COLUMN form_layout VARCHAR(5000) NULL;
-- COMMENT ON COLUMN gen_table.form_layout IS '表单布局配置（JSON格式）';
