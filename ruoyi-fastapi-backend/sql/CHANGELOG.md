# 数据库变更日志

## [2026-03-04] 系统品牌更新

### 变更说明
将系统名称从"优辰管理系统"统一更改为"宥辰开发平台"

### 变更详情

#### 数据库初始化脚本更新

##### 1. MySQL初始化脚本 (ruoyi-fastapi.sql)
- ✅ 更新 `sys_notice` 表初始化数据
  - 记录1: "温馨提醒：2018-07-01 宥辰开发平台新版本发布啦"
  - 记录2: "维护通知：2018-07-01 宥辰开发平台凌晨维护"
- ✅ 更新 `sys_menu` 表菜单ID 99
  - 菜单名称: "若依官网" → "官方网站"
  - 链接地址: "http://ruoyi.vip" → "https://youchen.dev"
  - 备注: "若依官网地址" → "宥辰开发平台官方网站"
- ✅ 新增 `sys_menu` 表技能管理菜单 (menu_id=120)
  - 菜单名称: "技能管理"
  - 路由地址: "skill"
  - 组件路径: "ai/skill/index"
  - 权限标识: "ai:skill:list"
- ✅ 新增技能管理按钮权限 (menu_id=1065, 1066)
  - 技能查询: "ai:skill:query"
  - 技能列表: "ai:skill:list"
- ✅ 更新 `sys_role_menu` 表，为普通角色(role_id=2)添加AI管理权限
  - 模型管理菜单及按钮 (118, 1061-1064)
  - AI对话菜单 (119)
  - 技能管理菜单及按钮 (120, 1065-1066)

##### 2. PostgreSQL初始化脚本 (ruoyi-fastapi-pg.sql)
- ✅ 更新 `sys_notice` 表初始化数据
  - 记录1: "温馨提醒：2018-07-01 宥辰开发平台新版本发布啦"
  - 记录2: "维护通知：2018-07-01 宥辰开发平台凌晨维护"
- ✅ 更新 `sys_menu` 表菜单ID 99
  - 菜单名称: "若依官网" → "官方网站"
  - 链接地址: "http://ruoyi.vip" → "https://youchen.dev"
  - 备注: "若依官网地址" → "宥辰开发平台官方网站"
- ✅ 新增 `sys_menu` 表技能管理菜单 (menu_id=120)
  - 菜单名称: "技能管理"
  - 路由地址: "skill"
  - 组件路径: "ai/skill/index"
  - 权限标识: "ai:skill:list"
- ✅ 新增技能管理按钮权限 (menu_id=1065, 1066)
  - 技能查询: "ai:skill:query"
  - 技能列表: "ai:skill:list"
- ✅ 更新 `sys_role_menu` 表，为普通角色(role_id=2)添加AI管理权限
  - 模型管理菜单及按钮 (118, 1061-1064)
  - AI对话菜单 (119)
  - 技能管理菜单及按钮 (120, 1065-1066)

##### 3. 新增增量更新脚本 (update_system_name.sql)
- ✅ 创建用于已有数据库的增量更新脚本
- ✅ 包含回滚方案和验证SQL

#### 前端配置文件更新

##### 环境配置文件
- ✅ `.env.development` - 开发环境
- ✅ `.env.production` - 生产环境
- ✅ `.env.staging` - 测试环境
- ✅ `.env.docker` - Docker环境
- ✅ `vue.config.js` - Vue配置

##### 页面文件
- ✅ `src/views/dashboard/index.vue` - 仪表盘系统版本显示
- ✅ `src/views/ui-showcase.vue` - UI展示页面标题

#### 后端文件更新
- ✅ `module_ai/skills/README.md` - AI技能系统文档

#### 项目文档更新
- ✅ `README.md` - 项目主文档标题和简介

### 影响范围

#### 数据库表
- `sys_notice` - 通知公告表 (2条记录)
- `sys_menu` - 菜单权限表 (4条记录：1条更新，1条新增菜单，2条新增按钮)
- `sys_role_menu` - 角色菜单关联表 (9条新增记录)

#### 配置文件
- 前端环境配置 (4个文件)
- 前端构建配置 (1个文件)
- 前端页面 (2个文件)

#### 文档文件
- 项目文档 (1个文件)
- 后端模块文档 (1个文件)

### 升级指南

#### 新项目部署
直接使用更新后的初始化脚本即可：
```bash
# MySQL
mysql -u root -p database_name < ruoyi-fastapi-backend/sql/ruoyi-fastapi.sql

# PostgreSQL
psql -U postgres -d database_name -f ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg.sql
```

#### 已有项目升级
1. 备份数据库
2. 执行增量更新脚本：
```bash
# MySQL
mysql -u root -p database_name < ruoyi-fastapi-backend/sql/update_system_name.sql

# PostgreSQL
psql -U postgres -d database_name -f ruoyi-fastapi-backend/sql/update_system_name.sql
```
3. 更新前端代码
4. 重启后端服务
5. 清除浏览器缓存

### 验证方法

#### 数据库验证
```sql
-- 验证通知公告
SELECT notice_id, notice_title FROM sys_notice WHERE notice_id IN (1, 2);

-- 验证菜单
SELECT menu_id, menu_name, path, remark FROM sys_menu WHERE menu_id = 99;
```

#### 前端验证
1. 检查浏览器标签页标题是否显示"宥辰开发平台"
2. 检查仪表盘页面系统版本是否显示"宥辰开发平台 v1.9.0"
3. 检查UI展示页面标题是否显示"宥辰开发平台 现代化设计系统"

### 回滚方案

如需回滚，请参考 `update_system_name.sql` 文件中的回滚SQL语句。

### 注意事项

1. ⚠️ 更新前务必备份数据库
2. ⚠️ 建议先在测试环境验证
3. ⚠️ 更新后需清除浏览器缓存
4. ⚠️ 更新后需重启后端服务
5. ℹ️ 如有自定义公告数据，请手动调整
6. ℹ️ 官网链接 `https://youchen.dev` 为示例，请根据实际情况修改

### 相关文件

- `ruoyi-fastapi-backend/sql/ruoyi-fastapi.sql` - MySQL初始化脚本
- `ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg.sql` - PostgreSQL初始化脚本
- `ruoyi-fastapi-backend/sql/update_system_name.sql` - 增量更新脚本
- `ruoyi-fastapi-backend/sql/README_UPDATE.md` - 详细更新说明

### 技术支持

如遇问题，请查看 `README_UPDATE.md` 或联系技术支持团队。
