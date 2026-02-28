DO $$
DECLARE
    parentId bigint;
BEGIN
    -- 菜单 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('学生信息', '2000', '1', 'students', 'stu/students/index', 1, 0, 'C', '0', '0', 'stu:students:list', '#', 'admin', current_timestamp, '', null, '学生信息菜单')
    returning menu_id into parentId;

    -- 按钮 SQL
    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('学生信息查询', parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'stu:students:query',        '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('学生信息新增', parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'stu:students:add',          '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('学生信息修改', parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'stu:students:edit',         '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('学生信息删除', parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'stu:students:remove',       '#', 'admin', current_timestamp, '', null, '');

    insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
    values('学生信息导出', parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'stu:students:export',       '#', 'admin', current_timestamp, '', null, '');
END $$;
