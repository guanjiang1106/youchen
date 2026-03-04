-- ====================================================
-- 更新系统名称：优辰管理系统 -> 宥辰开发平台
-- 更新日期：2026-03-04
-- 说明：此脚本用于更新数据库中所有包含系统名称的数据，并添加技能管理菜单
-- ====================================================

-- 1. 更新通知公告表中的系统名称
UPDATE sys_notice 
SET notice_title = '温馨提醒：2018-07-01 宥辰开发平台新版本发布啦' 
WHERE notice_id = 1 AND notice_title LIKE '%优辰管理系统%';

UPDATE sys_notice 
SET notice_title = '维护通知：2018-07-01 宥辰开发平台凌晨维护' 
WHERE notice_id = 2 AND notice_title LIKE '%优辰管理系统%';

-- 2. 更新菜单表中的若依官网为宥辰官网（可选，根据实际需求决定是否执行）
UPDATE sys_menu 
SET menu_name = '官方网站', 
    path = 'https://youchen.dev',
    remark = '宥辰开发平台官方网站'
WHERE menu_id = 99;

-- 3. 添加技能管理菜单（如果不存在）
-- 注意：如果使用最新的初始化脚本，此步骤可跳过
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
SELECT 120, '技能管理', 4, 3, 'skill', 'ai/skill/index', 1, 0, 'C', '0', '0', 'ai:skill:list', 'skill', 'admin', NOW(), '技能管理菜单'
WHERE NOT EXISTS (SELECT 1 FROM sys_menu WHERE menu_id = 120);

-- 4. 添加技能管理按钮权限（如果不存在）
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
SELECT 1065, '技能查询', 120, 1, '#', '', 1, 0, 'F', '0', '0', 'ai:skill:query', '#', 'admin', NOW(), ''
WHERE NOT EXISTS (SELECT 1 FROM sys_menu WHERE menu_id = 1065);

INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
SELECT 1066, '技能列表', 120, 2, '#', '', 1, 0, 'F', '0', '0', 'ai:skill:list', '#', 'admin', NOW(), ''
WHERE NOT EXISTS (SELECT 1 FROM sys_menu WHERE menu_id = 1066);

-- 5. 为普通角色添加AI管理权限（如果不存在）
INSERT INTO sys_role_menu (role_id, menu_id)
SELECT 2, 118 WHERE NOT EXISTS (SELECT 1 FROM sys_role_menu WHERE role_id = 2 AND menu_id = 118)
UNION ALL
SELECT 2, 119 WHERE NOT EXISTS (SELECT 1 FROM sys_role_menu WHERE role_id = 2 AND menu_id = 119)
UNION ALL
SELECT 2, 120 WHERE NOT EXISTS (SELECT 1 FROM sys_role_menu WHERE role_id = 2 AND menu_id = 120)
UNION ALL
SELECT 2, 1061 WHERE NOT EXISTS (SELECT 1 FROM sys_role_menu WHERE role_id = 2 AND menu_id = 1061)
UNION ALL
SELECT 2, 1062 WHERE NOT EXISTS (SELECT 1 FROM sys_role_menu WHERE role_id = 2 AND menu_id = 1062)
UNION ALL
SELECT 2, 1063 WHERE NOT EXISTS (SELECT 1 FROM sys_role_menu WHERE role_id = 2 AND menu_id = 1063)
UNION ALL
SELECT 2, 1064 WHERE NOT EXISTS (SELECT 1 FROM sys_role_menu WHERE role_id = 2 AND menu_id = 1064)
UNION ALL
SELECT 2, 1065 WHERE NOT EXISTS (SELECT 1 FROM sys_role_menu WHERE role_id = 2 AND menu_id = 1065)
UNION ALL
SELECT 2, 1066 WHERE NOT EXISTS (SELECT 1 FROM sys_role_menu WHERE role_id = 2 AND menu_id = 1066);

-- 执行完成后，请验证数据是否更新成功
SELECT '=== 验证通知公告 ===' as step;
SELECT notice_id, notice_title FROM sys_notice WHERE notice_id IN (1, 2);

SELECT '=== 验证菜单 ===' as step;
SELECT menu_id, menu_name, path FROM sys_menu WHERE menu_id = 99;

SELECT '=== 验证技能管理菜单 ===' as step;
SELECT menu_id, menu_name, parent_id, path, perms FROM sys_menu WHERE menu_id IN (120, 1065, 1066);

SELECT '=== 验证角色权限 ===' as step;
SELECT rm.role_id, r.role_name, m.menu_id, m.menu_name, m.perms 
FROM sys_role_menu rm
JOIN sys_role r ON rm.role_id = r.role_id
JOIN sys_menu m ON rm.menu_id = m.menu_id
WHERE rm.role_id = 2 AND m.menu_id IN (118, 119, 120, 1061, 1062, 1063, 1064, 1065, 1066)
ORDER BY m.menu_id;
