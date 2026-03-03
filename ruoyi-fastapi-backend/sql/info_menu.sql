DO $$
DECLARE
    parentId bigint;
BEGIN
    -- 菜单 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺信息', '2012', '1', 'info', 'module_admin/info/index', 1, 0, 'C', '0', '0', 'module_admin:info:list', '#', 'admin', current_timestamp, '', null, '工艺信息菜单')
    returning menu_id into parentId;

    -- 按钮 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺信息查询', parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:info:query',        '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺信息新增', parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:info:add',          '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺信息修改', parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:info:edit',         '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺信息删除', parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:info:remove',       '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('工艺信息导出', parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:info:export',       '#', 'admin', current_timestamp, '', null, '');
END $$;
