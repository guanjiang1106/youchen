-- 为 gen_table_column 表添加扩展字段
-- 用于支持关联表配置、页签配置等功能

-- MySQL 版本

-- 添加关联表字段
ALTER TABLE `gen_table_column` ADD COLUMN `link_table` VARCHAR(200) NULL COMMENT '关联表名称' AFTER `dict_type`;

-- 添加关联表标签字段
ALTER TABLE `gen_table_column` ADD COLUMN `link_label_field` VARCHAR(200) NULL COMMENT '关联表标签字段' AFTER `link_table`;

-- 添加关联表值字段
ALTER TABLE `gen_table_column` ADD COLUMN `link_value_field` VARCHAR(200) NULL COMMENT '关联表值字段' AFTER `link_label_field`;

-- 添加页签配置字段
ALTER TABLE `gen_table_column` ADD COLUMN `tab_page` VARCHAR(50) NULL DEFAULT 'basic' COMMENT '显示页签（basic基本信息/detail详细信息）' AFTER `link_value_field`;

-- 添加默认值字段
ALTER TABLE `gen_table_column` ADD COLUMN `default_value` VARCHAR(500) NULL COMMENT '默认值' AFTER `tab_page`;

-- 添加示例值字段
ALTER TABLE `gen_table_column` ADD COLUMN `example_value` VARCHAR(500) NULL COMMENT '示例值' AFTER `default_value`;

-- 添加列表宽度字段
ALTER TABLE `gen_table_column` ADD COLUMN `list_width` INT NULL COMMENT '列表显示宽度（像素）' AFTER `example_value`;
