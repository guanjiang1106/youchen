DO $$
DECLARE
    parentId bigint;
BEGIN
    -- 菜单 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺', '2000', '1', 'process', 'module_admin/process/index', 1, 0, 'C', '0', '0', 'module_admin:process:list', '#', 'admin', current_timestamp, '', null, '工艺菜单')
    returning menu_id into parentId;

    -- 按钮 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺查询', parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:process:query',        '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺新增', parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:process:add',          '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺修改', parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:process:edit',         '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺删除', parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:process:remove',       '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺导出', parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:process:export',       '#', 'admin', current_timestamp, '', null, '');
END $$;
