DO $$
DECLARE
    parentId bigint;
BEGIN
    -- 菜单 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('老师维护', '2000', '1', 'teacher', 'module_admin/teacher/index', 1, 0, 'C', '0', '0', 'module_admin:teacher:list', '#', 'admin', current_timestamp, '', null, '老师维护菜单')
    returning menu_id into parentId;

    -- 按钮 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('老师维护查询', parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:teacher:query',        '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('老师维护新增', parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:teacher:add',          '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('老师维护修改', parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:teacher:edit',         '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('老师维护删除', parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:teacher:remove',       '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('老师维护导出', parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:teacher:export',       '#', 'admin', current_timestamp, '', null, '');
END $$;
