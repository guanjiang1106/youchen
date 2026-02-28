DO $$
DECLARE
    parentId bigint;
BEGIN
    -- 菜单 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('物料', '2000', '1', 'material', 'module_admin/material/index', 1, 0, 'C', '0', '0', 'module_admin:material:list', '#', 'admin', current_timestamp, '', null, '物料菜单')
    returning menu_id into parentId;

    -- 按钮 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('物料查询', parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:material:query',        '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('物料新增', parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:material:add',          '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('物料修改', parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:material:edit',         '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('物料删除', parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:material:remove',       '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('物料导出', parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:material:export',       '#', 'admin', current_timestamp, '', null, '');
END $$;
