# 数据库更新说明

## 系统名称变更：优辰管理系统 → 宥辰开发平台

### 更新日期
2026-03-04

### 更新内容

本次更新将系统名称从"优辰管理系统"统一更改为"宥辰开发平台"，涉及以下数据库表：

#### 1. 通知公告表 (sys_notice)
- 记录ID 1: 温馨提醒公告标题
- 记录ID 2: 维护通知公告标题

#### 2. 菜单权限表 (sys_menu)  
- 菜单ID 99: 将"若依官网"更新为"官方网站"，链接更新为宥辰开发平台官网
- 菜单ID 120: 新增"技能管理"菜单（AI管理下的子菜单）
- 菜单ID 1065-1066: 新增技能管理的按钮权限（技能查询、技能列表）

#### 3. 角色菜单关联表 (sys_role_menu)
- 为普通角色(role_id=2)添加AI管理相关权限
  - 模型管理菜单及按钮权限
  - AI对话菜单权限
  - 技能管理菜单及按钮权限

### 更新方式

#### 方式一：全新安装（推荐）
如果是全新安装系统，直接使用更新后的初始化脚本：

**MySQL数据库：**
```bash
mysql -u root -p your_database < ruoyi-fastapi-backend/sql/ruoyi-fastapi.sql
```

**PostgreSQL数据库：**
```bash
psql -U postgres -d your_database -f ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg.sql
```

#### 方式二：已有数据库更新
如果已经有运行中的数据库，使用增量更新脚本：

**MySQL/PostgreSQL通用：**
```bash
# MySQL
mysql -u root -p your_database < ruoyi-fastapi-backend/sql/update_system_name.sql

# PostgreSQL  
psql -U postgres -d your_database -f ruoyi-fastapi-backend/sql/update_system_name.sql
```

或者手动执行以下SQL语句：

```sql
-- 更新通知公告
UPDATE sys_notice 
SET notice_title = '温馨提醒：2018-07-01 宥辰开发平台新版本发布啦' 
WHERE notice_id = 1;

UPDATE sys_notice 
SET notice_title = '维护通知：2018-07-01 宥辰开发平台凌晨维护' 
WHERE notice_id = 2;

-- 更新菜单（可选）
UPDATE sys_menu 
SET menu_name = '官方网站', 
    path = 'https://youchen.dev',
    remark = '宥辰开发平台官方网站'
WHERE menu_id = 99;

-- 新增技能管理菜单（如果使用的是旧版初始化脚本）
-- 注意：新版初始化脚本已包含此菜单，无需手动添加
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES (120, '技能管理', 4, 3, 'skill', 'ai/skill/index', 1, 0, 'C', '0', '0', 'ai:skill:list', 'skill', 'admin', NOW(), '技能管理菜单');

-- 新增技能管理按钮权限
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, remark)
VALUES 
(1065, '技能查询', 120, 1, '#', '', 1, 0, 'F', '0', '0', 'ai:skill:query', '#', 'admin', NOW(), ''),
(1066, '技能列表', 120, 2, '#', '', 1, 0, 'F', '0', '0', 'ai:skill:list', '#', 'admin', NOW(), '');

-- 为普通角色添加AI管理权限
INSERT INTO sys_role_menu (role_id, menu_id) VALUES
(2, 118), (2, 119), (2, 120),
(2, 1061), (2, 1062), (2, 1063), (2, 1064),
(2, 1065), (2, 1066);
```

### 验证更新

执行以下SQL验证更新是否成功：

```sql
-- 检查通知公告
SELECT notice_id, notice_title FROM sys_notice WHERE notice_id IN (1, 2);

-- 检查菜单
SELECT menu_id, menu_name, path FROM sys_menu WHERE menu_id = 99;

-- 检查技能管理菜单
SELECT menu_id, menu_name, parent_id, path, perms FROM sys_menu WHERE menu_id IN (120, 1065, 1066);

-- 检查角色权限
SELECT r.role_name, m.menu_name, m.perms 
FROM sys_role_menu rm
JOIN sys_role r ON rm.role_id = r.role_id
JOIN sys_menu m ON rm.menu_id = m.menu_id
WHERE rm.role_id = 2 AND m.menu_id IN (118, 119, 120, 1061, 1062, 1063, 1064, 1065, 1066);
```

### 相关文件更新

除了数据库脚本，以下文件也已同步更新系统名称：

#### 前端文件
- `ruoyi-fastapi-frontend/.env.development` - 开发环境配置
- `ruoyi-fastapi-frontend/.env.production` - 生产环境配置
- `ruoyi-fastapi-frontend/.env.staging` - 测试环境配置
- `ruoyi-fastapi-frontend/.env.docker` - Docker环境配置
- `ruoyi-fastapi-frontend/vue.config.js` - Vue配置文件
- `ruoyi-fastapi-frontend/src/views/dashboard/index.vue` - 仪表盘页面
- `ruoyi-fastapi-frontend/src/views/ui-showcase.vue` - UI展示页面

#### 后端文件
- `ruoyi-fastapi-backend/module_ai/skills/README.md` - AI技能系统文档

#### 项目文档
- `README.md` - 项目主文档

### 注意事项

1. 更新前请务必备份数据库
2. 建议在测试环境先执行更新，验证无误后再在生产环境执行
3. 如果有自定义的公告或菜单数据，请根据实际情况调整SQL语句
4. 更新后需要清除浏览器缓存和重启后端服务才能看到完整效果

### 回滚方案

如需回滚到原系统名称，执行以下SQL：

```sql
-- 回滚通知公告
UPDATE sys_notice 
SET notice_title = '温馨提醒：2018-07-01 优辰管理系统新版本发布啦' 
WHERE notice_id = 1;

UPDATE sys_notice 
SET notice_title = '维护通知：2018-07-01 优辰管理系统凌晨维护' 
WHERE notice_id = 2;

-- 回滚菜单
UPDATE sys_menu 
SET menu_name = '若依官网', 
    path = 'http://ruoyi.vip',
    remark = '若依官网地址'
WHERE menu_id = 99;
```

### 技术支持

如有问题，请联系技术支持团队或查看项目文档。
