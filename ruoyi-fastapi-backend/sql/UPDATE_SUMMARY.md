# 数据库更新总结

## 更新日期
2026-03-04

## 更新内容概览

本次更新主要完成两项任务:
1. **系统品牌更新**: 将"优辰管理系统"统一更改为"宥辰开发平台"
2. **AI功能完善**: 将技能管理菜单整合到主初始化脚本中

---

## 一、系统品牌更新

### 更新范围

#### 前端文件 (8个)
✅ 环境配置文件
- `.env.development` - 开发环境
- `.env.production` - 生产环境
- `.env.staging` - 测试环境
- `.env.docker` - Docker环境

✅ 配置和页面文件
- `vue.config.js` - Vue配置
- `src/views/dashboard/index.vue` - 仪表盘
- `src/views/ui-showcase.vue` - UI展示

#### 后端文件 (3个)
✅ SQL初始化脚本
- `sql/ruoyi-fastapi.sql` - MySQL版本
- `sql/ruoyi-fastapi-pg.sql` - PostgreSQL版本

✅ 文档文件
- `module_ai/skills/README.md` - AI技能系统文档

#### 项目文档 (1个)
✅ `README.md` - 项目主文档

### 数据库变更

#### 1. sys_notice (通知公告表)
```sql
-- 记录1
旧: "温馨提醒：2018-07-01 优辰管理系统新版本发布啦"
新: "温馨提醒：2018-07-01 宥辰开发平台新版本发布啦"

-- 记录2
旧: "维护通知：2018-07-01 优辰管理系统凌晨维护"
新: "维护通知：2018-07-01 宥辰开发平台凌晨维护"
```

#### 2. sys_menu (菜单权限表)
```sql
-- 菜单ID 99
旧: 菜单名称="若依官网", 链接="http://ruoyi.vip"
新: 菜单名称="官方网站", 链接="https://youchen.dev"
```

---

## 二、AI功能完善

### 新增菜单

#### 1. 技能管理主菜单 (menu_id=120)
```sql
菜单名称: 技能管理
父菜单ID: 4 (AI 管理)
排序号: 3
路由地址: skill
组件路径: ai/skill/index
权限标识: ai:skill:list
图标: skill
菜单类型: C (菜单)
```

#### 2. 技能管理按钮权限

**技能查询 (menu_id=1065)**
```sql
父菜单ID: 120
权限标识: ai:skill:query
菜单类型: F (按钮)
```

**技能列表 (menu_id=1066)**
```sql
父菜单ID: 120
权限标识: ai:skill:list
菜单类型: F (按钮)
```

### 角色权限更新

为普通角色(role_id=2)新增以下权限:

| 菜单ID | 菜单名称 | 权限标识 | 类型 |
|--------|----------|----------|------|
| 118 | 模型管理 | ai:model:list | 菜单 |
| 119 | AI 对话 | ai:chat:list | 菜单 |
| 120 | 技能管理 | ai:skill:list | 菜单 |
| 1061 | 模型查询 | ai:model:query | 按钮 |
| 1062 | 模型新增 | ai:model:add | 按钮 |
| 1063 | 模型修改 | ai:model:edit | 按钮 |
| 1064 | 模型删除 | ai:model:remove | 按钮 |
| 1065 | 技能查询 | ai:skill:query | 按钮 |
| 1066 | 技能列表 | ai:skill:list | 按钮 |

---

## 三、更新后的AI管理菜单结构

```
AI 管理 (menu_id=4)
├── 模型管理 (menu_id=118)
│   ├── 模型查询 (1061)
│   ├── 模型新增 (1062)
│   ├── 模型修改 (1063)
│   └── 模型删除 (1064)
├── AI 对话 (menu_id=119)
└── 技能管理 (menu_id=120) ⭐ 新增
    ├── 技能查询 (1065) ⭐ 新增
    └── 技能列表 (1066) ⭐ 新增
```

---

## 四、文件清单

### 新增文件 (4个)
1. `sql/update_system_name.sql` - 增量更新脚本
2. `sql/README_UPDATE.md` - 详细更新说明
3. `sql/CHANGELOG.md` - 变更日志
4. `sql/AI_FEATURES_INIT.md` - AI功能初始化说明
5. `sql/UPDATE_SUMMARY.md` - 本文件

### 修改文件 (14个)

**前端 (7个)**
- `ruoyi-fastapi-frontend/.env.development`
- `ruoyi-fastapi-frontend/.env.production`
- `ruoyi-fastapi-frontend/.env.staging`
- `ruoyi-fastapi-frontend/.env.docker`
- `ruoyi-fastapi-frontend/vue.config.js`
- `ruoyi-fastapi-frontend/src/views/dashboard/index.vue`
- `ruoyi-fastapi-frontend/src/views/ui-showcase.vue`

**后端 (3个)**
- `ruoyi-fastapi-backend/sql/ruoyi-fastapi.sql`
- `ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg.sql`
- `ruoyi-fastapi-backend/module_ai/skills/README.md`

**文档 (1个)**
- `README.md`

### 保留文件 (1个)
- `sql/add_skill_management_menu.sql` - 旧版独立脚本(已整合到主脚本,保留作为参考)

---

## 五、部署指南

### 新项目部署

直接使用更新后的初始化脚本:

```bash
# MySQL
mysql -u root -p database_name < ruoyi-fastapi-backend/sql/ruoyi-fastapi.sql

# PostgreSQL
psql -U postgres -d database_name -f ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg.sql
```

### 已有项目升级

#### 步骤1: 备份数据库
```bash
# MySQL
mysqldump -u root -p database_name > backup_$(date +%Y%m%d).sql

# PostgreSQL
pg_dump -U postgres database_name > backup_$(date +%Y%m%d).sql
```

#### 步骤2: 执行增量更新
```bash
# MySQL
mysql -u root -p database_name < ruoyi-fastapi-backend/sql/update_system_name.sql

# PostgreSQL
psql -U postgres -d database_name -f ruoyi-fastapi-backend/sql/update_system_name.sql
```

#### 步骤3: 验证更新
```sql
-- 验证通知公告
SELECT notice_id, notice_title FROM sys_notice WHERE notice_id IN (1, 2);

-- 验证菜单
SELECT menu_id, menu_name, path FROM sys_menu WHERE menu_id IN (99, 120);

-- 验证技能管理按钮
SELECT menu_id, menu_name, perms FROM sys_menu WHERE menu_id IN (1065, 1066);

-- 验证角色权限
SELECT COUNT(*) as count FROM sys_role_menu 
WHERE role_id = 2 AND menu_id IN (118, 119, 120, 1061, 1062, 1063, 1064, 1065, 1066);
-- 应该返回 9
```

#### 步骤4: 更新代码
```bash
# 拉取最新代码
git pull origin main

# 安装依赖(如有更新)
cd ruoyi-fastapi-frontend
npm install

cd ../ruoyi-fastapi-backend
pip install -r requirements.txt
```

#### 步骤5: 重启服务
```bash
# 重启后端
# 根据实际部署方式重启

# 重新构建前端
cd ruoyi-fastapi-frontend
npm run build
```

#### 步骤6: 清除缓存
- 清除浏览器缓存
- 清除Redis缓存(如有)
- 重新登录系统

---

## 六、验证清单

### 数据库验证
- [ ] 通知公告标题已更新为"宥辰开发平台"
- [ ] 菜单99已更新为"官方网站"
- [ ] 技能管理菜单(120)已添加
- [ ] 技能管理按钮(1065, 1066)已添加
- [ ] 普通角色已有AI管理权限

### 前端验证
- [ ] 浏览器标签页显示"宥辰开发平台"
- [ ] 仪表盘显示"宥辰开发平台 v1.9.0"
- [ ] 左侧菜单显示"AI 管理"
- [ ] AI 管理下显示"技能管理"菜单
- [ ] 点击技能管理可正常访问

### 后端验证
- [ ] 技能管理接口可正常访问
- [ ] 权限验证正常工作
- [ ] 日志中无错误信息

---

## 七、回滚方案

如需回滚,请执行以下SQL:

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

-- 删除技能管理菜单(可选)
DELETE FROM sys_role_menu WHERE menu_id IN (120, 1065, 1066);
DELETE FROM sys_menu WHERE menu_id IN (120, 1065, 1066);
```

---

## 八、注意事项

1. ⚠️ **备份优先**: 更新前务必备份数据库
2. ⚠️ **测试环境**: 建议先在测试环境验证
3. ⚠️ **清除缓存**: 更新后需清除浏览器缓存
4. ⚠️ **重启服务**: 更新后需重启后端服务
5. ℹ️ **官网链接**: `https://youchen.dev` 为示例,请根据实际修改
6. ℹ️ **权限检查**: 确认用户角色有相应权限
7. ℹ️ **前端页面**: 确保前端技能管理页面已开发完成

---

## 九、技术支持

### 相关文档
- `README_UPDATE.md` - 详细更新操作指南
- `CHANGELOG.md` - 完整变更日志
- `AI_FEATURES_INIT.md` - AI功能初始化说明
- `update_system_name.sql` - 增量更新脚本

### 常见问题
请参考 `AI_FEATURES_INIT.md` 中的"常见问题"章节。

### 联系方式
如有问题,请联系技术支持团队或查看项目文档。

---

**更新完成时间**: 2026-03-04  
**文档版本**: v1.0  
**适用版本**: 宥辰开发平台 v1.9.0+
