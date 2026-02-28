-- 新增物料状态字典示例
-- 在数据库中执行此 SQL

-- 1. 新增字典类型
INSERT INTO sys_dict_type (dict_name, dict_type, status, create_by, create_time, remark)
VALUES ('物料状态', 'material_status', '0', 'admin', CURRENT_TIMESTAMP, '物料的启用禁用状态');

-- 2. 新增字典数据（获取刚插入的字典类型ID）
-- PostgreSQL 版本
INSERT INTO sys_dict_data (dict_sort, dict_label, dict_value, dict_type, css_class, list_class, is_default, status, create_by, create_time, remark)
VALUES 
  (1, '启用', '1', 'material_status', '', 'success', 'Y', '0', 'admin', CURRENT_TIMESTAMP, '物料启用状态'),
  (2, '禁用', '0', 'material_status', '', 'danger', 'N', '0', 'admin', CURRENT_TIMESTAMP, '物料禁用状态');

-- MySQL 版本（如果使用 MySQL）
-- INSERT INTO sys_dict_data (dict_sort, dict_label, dict_value, dict_type, css_class, list_class, is_default, status, create_by, create_time, remark)
-- VALUES 
--   (1, '启用', '1', 'material_status', '', 'success', 'Y', '0', 'admin', now(), '物料启用状态'),
--   (2, '禁用', '0', 'material_status', '', 'danger', 'N', '0', 'admin', now(), '物料禁用状态');
