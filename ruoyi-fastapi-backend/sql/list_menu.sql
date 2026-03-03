DO $$
DECLARE
    parentId bigint;
BEGIN
    -- 菜单 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('设备清单', '2012', '1', 'list', 'module_admin/list/index', 1, 0, 'C', '0', '0', 'module_admin:list:list', '#', 'admin', current_timestamp, '', null, '设备清单菜单')
    returning menu_id into parentId;

    -- 按钮 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('设备清单查询', parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:list:query',        '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('设备清单新增', parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:list:add',          '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('设备清单修改', parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:list:edit',         '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('设备清单删除', parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:list:remove',       '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('设备清单导出', parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:list:export',       '#', 'admin', current_timestamp, '', null, '');
END $$;
