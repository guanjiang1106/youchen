DO $$
DECLARE
    parentId bigint;
BEGIN
    -- 菜单 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('质量检验记录', '2012', '1', 'table', 'module_admin/table/index', 1, 0, 'C', '0', '0', 'module_admin:table:list', '#', 'admin', current_timestamp, '', null, '质量检验记录菜单')
    returning menu_id into parentId;

    -- 按钮 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('质量检验记录查询', parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:table:query',        '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('质量检验记录新增', parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:table:add',          '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('质量检验记录修改', parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:table:edit',         '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('质量检验记录删除', parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:table:remove',       '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('质量检验记录导出', parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'module_admin:table:export',       '#', 'admin', current_timestamp, '', null, '');
END $$;
