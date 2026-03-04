-- =============================================
-- AI 技能管理菜单添加脚本
-- =============================================

-- 1. 查找 AI 管理的父菜单 ID
SET @ai_parent_id = (SELECT menu_id FROM sys_menu WHERE menu_name = 'AI管理' LIMIT 1);

-- 2. 添加技能管理菜单（主菜单）
INSERT INTO sys_menu (
    menu_name, 
    parent_id, 
    order_num, 
    path, 
    component, 
    is_frame, 
    is_cache, 
    menu_type, 
    visible, 
    status, 
    perms, 
    icon, 
    create_by, 
    create_time, 
    remark
)
VALUES (
    '技能管理',           -- 菜单名称
    @ai_parent_id,        -- 父菜单ID（AI管理）
    3,                    -- 排序号
    'skill',              -- 路由地址
    'ai/skill/index',     -- 组件路径
    1,                    -- 是否为外链（1否 0是）
    0,                    -- 是否缓存（0缓存 1不缓存）
    'C',                  -- 菜单类型（M目录 C菜单 F按钮）
    '0',                  -- 显示状态（0显示 1隐藏）
    '0',                  -- 菜单状态（0正常 1停用）
    'ai:skill:list',      -- 权限标识
    'skill',              -- 菜单图标
    'admin',              -- 创建者
    NOW(),                -- 创建时间
    'AI技能管理菜单'      -- 备注
);

-- 获取刚插入的技能管理菜单ID
SET @skill_menu_id = LAST_INSERT_ID();

-- 3. 添加技能管理的按钮权限

-- 3.1 查询按钮
INSERT INTO sys_menu (
    menu_name, 
    parent_id, 
    order_num, 
    path, 
    component, 
    is_frame, 
    is_cache, 
    menu_type, 
    visible, 
    status, 
    perms, 
    icon, 
    create_by, 
    create_time, 
    remark
)
VALUES (
    '技能查询',
    @skill_menu_id,
    1,
    '#',
    '',
    1,
    0,
    'F',
    '0',
    '0',
    'ai:skill:query',
    '#',
    'admin',
    NOW(),
    '技能查询按钮'
);

-- 3.2 统计按钮
INSERT INTO sys_menu (
    menu_name, 
    parent_id, 
    order_num, 
    path, 
    component, 
    is_frame, 
    is_cache, 
    menu_type, 
    visible, 
    status, 
    perms, 
    icon, 
    create_by, 
    create_time, 
    remark
)
VALUES (
    '技能统计',
    @skill_menu_id,
    2,
    '#',
    '',
    1,
    0,
    'F',
    '0',
    '0',
    'ai:skill:stats',
    '#',
    'admin',
    NOW(),
    '技能统计按钮'
);

-- 4. 为管理员角色分配权限（假设管理员角色ID为1）
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT 1, menu_id 
FROM sys_menu 
WHERE menu_name IN ('技能管理', '技能查询', '技能统计')
AND parent_id = @skill_menu_id OR menu_id = @skill_menu_id;

-- 5. 验证插入结果
SELECT 
    m.menu_id,
    m.menu_name,
    m.parent_id,
    m.order_num,
    m.path,
    m.component,
    m.menu_type,
    m.perms,
    m.icon,
    p.menu_name as parent_name
FROM sys_menu m
LEFT JOIN sys_menu p ON m.parent_id = p.menu_id
WHERE m.menu_name IN ('技能管理', '技能查询', '技能统计')
ORDER BY m.parent_id, m.order_num;

-- 完成提示
SELECT '✅ 技能管理菜单添加成功！' as message;
SELECT '📝 请刷新页面查看新菜单' as tip;
