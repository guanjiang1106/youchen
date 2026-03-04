# AI 功能菜单初始化说明

## 概述

本文档说明宥辰开发平台中AI管理模块的菜单初始化情况。

## AI 管理菜单结构

### 一级菜单
- **菜单ID**: 4
- **菜单名称**: AI 管理
- **路由地址**: ai
- **图标**: ai-manage
- **状态**: 正常显示

### 二级菜单

#### 1. 模型管理 (menu_id=118)
- **路由地址**: model
- **组件路径**: ai/model/index
- **权限标识**: ai:model:list
- **图标**: ai-model
- **功能说明**: 管理AI模型配置，包括模型提供商、API密钥等

**按钮权限**:
- 模型查询 (1061): ai:model:query
- 模型新增 (1062): ai:model:add
- 模型修改 (1063): ai:model:edit
- 模型删除 (1064): ai:model:remove

#### 2. AI 对话 (menu_id=119)
- **路由地址**: chat
- **组件路径**: ai/chat/index
- **权限标识**: ai:chat:list
- **图标**: ai-chat
- **功能说明**: AI对话交互界面，支持多轮对话

#### 3. 技能管理 (menu_id=120) ⭐ 新增
- **路由地址**: skill
- **组件路径**: ai/skill/index
- **权限标识**: ai:skill:list
- **图标**: skill
- **功能说明**: 管理AI技能，查看技能列表、统计信息等

**按钮权限**:
- 技能查询 (1065): ai:skill:query
- 技能列表 (1066): ai:skill:list

## 初始化状态

### 最新版本 (2026-03-04)

✅ **已包含在主初始化脚本中**:
- `ruoyi-fastapi.sql` (MySQL)
- `ruoyi-fastapi-pg.sql` (PostgreSQL)

以下菜单和权限已自动初始化:
1. AI 管理目录 (menu_id=4)
2. 模型管理菜单及按钮 (118, 1061-1064)
3. AI 对话菜单 (119)
4. 技能管理菜单及按钮 (120, 1065-1066) ⭐ 新增

### 旧版本升级

如果使用的是旧版初始化脚本（2026-03-04之前），需要执行以下操作:

#### 方式一：使用增量更新脚本
```bash
# MySQL
mysql -u root -p database_name < ruoyi-fastapi-backend/sql/update_system_name.sql

# PostgreSQL
psql -U postgres -d database_name -f ruoyi-fastapi-backend/sql/update_system_name.sql
```

#### 方式二：手动执行SQL
参考 `update_system_name.sql` 文件中的SQL语句。

## 角色权限配置

### 超级管理员 (role_id=1)
- 拥有所有菜单和按钮权限（默认）

### 普通角色 (role_id=2)
已自动分配以下AI管理权限:
- 模型管理菜单 (118)
- AI对话菜单 (119)
- 技能管理菜单 (120) ⭐ 新增
- 所有相关按钮权限 (1061-1066)

## 后端接口对应关系

### 模型管理 (ai_model_controller.py)
- 路由前缀: `/ai/model`
- 权限标识: `ai:model:*`

### AI 对话 (ai_chat_controller.py)
- 路由前缀: `/ai/chat`
- 权限标识: `ai:chat:*`

### 技能管理 (ai_skill_controller.py)
- 路由前缀: `/ai/skill`
- 权限标识: `ai:skill:*`
- 主要接口:
  - GET `/ai/skill/list` - 获取技能列表
  - GET `/ai/skill/{skill_name}` - 获取技能详情
  - GET `/ai/skill/stats` - 获取技能统计
  - GET `/ai/skill/prompt` - 获取技能提示词

## 前端页面对应关系

### 模型管理
- 页面路径: `ruoyi-fastapi-frontend/src/views/ai/model/index.vue`
- 路由: `/ai/model`

### AI 对话
- 页面路径: `ruoyi-fastapi-frontend/src/views/ai/chat/index.vue`
- 路由: `/ai/chat`

### 技能管理
- 页面路径: `ruoyi-fastapi-frontend/src/views/ai/skill/index.vue`
- 路由: `/ai/skill`

## 数据库表结构

### AI模型表 (ai_models)
存储AI模型配置信息，包括:
- 模型ID、名称、提供商
- API配置信息
- 模型参数设置

### AI对话配置表 (ai_chat_config)
存储AI对话相关配置，包括:
- 对话配置ID
- 系统提示词
- 对话参数设置

### 技能数据
技能管理功能基于文件系统，技能定义存储在:
- `ruoyi-fastapi-backend/module_ai/skills/bundled/`

## 验证方法

### 1. 数据库验证
```sql
-- 查看AI管理菜单结构
SELECT 
    m.menu_id,
    m.menu_name,
    m.parent_id,
    m.order_num,
    m.path,
    m.component,
    m.menu_type,
    m.perms,
    p.menu_name as parent_name
FROM sys_menu m
LEFT JOIN sys_menu p ON m.parent_id = p.menu_id
WHERE m.parent_id = 4 OR m.menu_id = 4
ORDER BY m.parent_id, m.order_num;

-- 查看普通角色的AI权限
SELECT 
    r.role_name,
    m.menu_name,
    m.perms,
    m.menu_type
FROM sys_role_menu rm
JOIN sys_role r ON rm.role_id = r.role_id
JOIN sys_menu m ON rm.menu_id = m.menu_id
WHERE rm.role_id = 2 
  AND (m.parent_id = 4 OR m.menu_id = 4 OR m.parent_id IN (118, 119, 120))
ORDER BY m.menu_id;
```

### 2. 前端验证
1. 使用普通角色账号登录系统
2. 检查左侧菜单是否显示"AI 管理"
3. 展开"AI 管理"，应该看到:
   - 模型管理
   - AI 对话
   - 技能管理 ⭐
4. 点击"技能管理"，应该能正常访问页面

### 3. 接口验证
```bash
# 获取技能列表
curl -X GET "http://localhost:8000/ai/skill/list" \
  -H "Authorization: Bearer {token}"

# 获取技能统计
curl -X GET "http://localhost:8000/ai/skill/stats" \
  -H "Authorization: Bearer {token}"
```

## 常见问题

### Q1: 技能管理菜单不显示？
**A**: 检查以下几点:
1. 数据库中是否存在 menu_id=120 的记录
2. 当前角色是否有该菜单权限（sys_role_menu表）
3. 菜单状态是否为正常（status='0'）
4. 清除浏览器缓存后重新登录

### Q2: 点击技能管理报404错误？
**A**: 检查前端路由配置:
1. 确认 `src/views/ai/skill/index.vue` 文件存在
2. 检查路由配置是否正确
3. 重新构建前端项目

### Q3: 技能管理接口返回403无权限？
**A**: 检查权限配置:
1. 确认用户角色有 `ai:skill:list` 权限
2. 检查接口装饰器中的权限标识是否正确
3. 确认token有效且未过期

### Q4: 旧版本如何升级？
**A**: 执行以下步骤:
1. 备份数据库
2. 执行 `update_system_name.sql` 脚本
3. 验证菜单和权限是否正确添加
4. 更新前端代码
5. 重启后端服务
6. 清除浏览器缓存

## 相关文件

- 主初始化脚本: `ruoyi-fastapi.sql`, `ruoyi-fastapi-pg.sql`
- 增量更新脚本: `update_system_name.sql`
- 变更日志: `CHANGELOG.md`
- 更新说明: `README_UPDATE.md`
- 后端控制器: `module_ai/controller/ai_skill_controller.py`
- 前端页面: `ruoyi-fastapi-frontend/src/views/ai/skill/index.vue`

## 技术支持

如有问题，请查看相关文档或联系技术支持团队。
