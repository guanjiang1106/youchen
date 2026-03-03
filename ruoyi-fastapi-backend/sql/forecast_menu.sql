DO $$
DECLARE
    parentId bigint;
BEGIN
    -- 菜单 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('销售预测，存储各产品在各区域的销售预测数据', '2012', '1', 'forecast', 'module_admin/forecast/index', 1, 0, 'C', '0', '0', 'module_admin:forecast:list', '#', 'admin', current_timestamp, '', null, '销售预测，存储各产品在各区域的销售预测数据菜单')
    returning menu_id into parentId;

    -- 按钮 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('销售预测，存储各产品在各区域的销售预测数据查询', parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:forecast:query',        '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('销售预测，存储各产品在各区域的销售预测数据新增', parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:forecast:add',          '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('销售预测，存储各产品在各区域的销售预测数据修改', parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:forecast:edit',         '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('销售预测，存储各产品在各区域的销售预测数据删除', parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:forecast:remove',       '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('销售预测，存储各产品在各区域的销售预测数据导出', parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:forecast:export',       '#', 'admin', current_timestamp, '', null, '');
END $$;
