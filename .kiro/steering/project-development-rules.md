---
inclusion: always
---

# RuoYi-FastAPI 项目开发规则

> 核心原则：新增功能，不改框架！业务代码放 `module_business`，系统代码在 `module_admin`

---

## 一、禁止修改区域（框架核心）

以下目录和文件是框架核心，禁止修改：

| 类型 | 路径 | 说明 |
|------|------|------|
| 应用入口 | `app.py`, `server.py` | 应用启动文件 |
| 配置管理 | `config/` | 数据库、Redis、环境配置 |
| 公共组件 | `common/` | 框架基础组件 |
| 异常处理 | `exceptions/` | 全局异常处理 |
| 中间件 | `middlewares/` | 请求拦截器 |
| 工具类 | `utils/` | 通用工具方法 |
| 系统模块 | `module_admin/` | 用户、角色、菜单等系统功能 |
| 任务模块 | `module_task/` | 定时任务 |
| 生成器 | `module_generator/` | 代码生成器 |
| 数据库迁移 | `alembic/` | 数据库版本管理 |

**可以修改的配置文件：**
- `.env.*` 文件中的配置值（如数据库地址、端口等）

---

## 二、新增功能开发流程

### 方式一：使用代码生成器（强烈推荐）

适用于标准的增删改查功能，一键生成前后端代码。

**步骤：**

1. 创建数据库表（必须包含审计字段）
2. 登录系统后台 → 系统工具 → 代码生成
3. 导入表 → 配置生成信息 → 生成代码
4. 在菜单管理中配置菜单和权限
5. 重启服务测试

**生成的代码包含：**
- 完整的 CRUD 接口
- 权限控制和日志记录
- Excel 导出功能
- 前端页面和 API

### 方式二：手动创建模块

适用于复杂业务逻辑，需要自定义实现。

**目录结构：**

```
module_business/              # 所有业务代码放这里
└── [业务名]/                # 如：product, order
    ├── controller/          # API 接口层
    │   └── [业务]_controller.py
    ├── service/             # 业务逻辑层
    │   └── [业务]_service.py
    ├── dao/                 # 数据库操作层
    │   └── [业务]_dao.py
    └── entity/              # 数据模型层
        ├── do/              # 数据库实体
        │   └── [业务]_do.py
        └── vo/              # 视图对象
            └── [业务]_vo.py
```

**模块说明：**
- `module_business/` - 业务代码（可修改）
- `module_admin/` - 系统代码（禁止修改）

---

## 三、命名规范

### 文件命名

| 层级 | 命名格式 | 示例 |
|------|----------|------|
| Controller | `[业务名]_controller.py` | `product_controller.py` |
| Service | `[业务名]_service.py` | `product_service.py` |
| DAO | `[业务名]_dao.py` | `product_dao.py` |
| DO | `[业务名]_do.py` | `product_do.py` |
| VO | `[业务名]_vo.py` | `product_vo.py` |

### 类命名

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| Service | `[业务名]Service` | `ProductService` |
| DAO | `[业务名]Dao` | `ProductDao` |
| DO | `[业务名]` | `BizProduct` |
| VO | `[业务名]Model` | `ProductModel` |

### 路由命名

```python
# 路由对象命名：[业务名]_controller
product_controller = APIRouterPro(
    prefix='/business/product',      # 路由前缀
    order_num=100,                   # 排序号（系统模块用1-20，业务模块从100开始）
    tags=['业务管理-产品管理'],       # API 分组标签
    dependencies=[PreAuthDependency()]  # 权限依赖
)
```

### 权限标识

格式：`模块:功能:操作`

| 操作 | 权限标识 | 说明 |
|------|----------|------|
| 列表查询 | `business:product:list` | 查看产品列表 |
| 新增 | `business:product:add` | 新增产品 |
| 编辑 | `business:product:edit` | 编辑产品 |
| 删除 | `business:product:remove` | 删除产品 |
| 导出 | `business:product:export` | 导出产品数据 |

---

## 四、代码规范

### Python 代码规范

| 规范项 | 要求 | 示例 |
|--------|------|------|
| 行长度 | 最多 120 字符 | - |
| 引号 | 单引号 `'` | `name = 'product'` |
| 类名 | 大驼峰 PascalCase | `ProductService` |
| 函数名 | 下划线 snake_case | `get_product_list` |
| 常量 | 全大写 UPPER_CASE | `MAX_SIZE = 100` |
| 类型注解 | 必须添加 | `def get_list() -> list:` |

### 数据库操作规范

**必须使用事务：**

```python
try:
    await ProductDao.add_product(query_db, obj)
    await query_db.commit()  # 提交事务
    return CrudResponseModel(is_success=True, message='操作成功')
except Exception as e:
    await query_db.rollback()  # 回滚事务
    raise e
```

**查询规范：**
- 使用 `select().where()` 而不是 `filter()`
- 分页查询使用 `PageUtil.paginate()`

### API 接口规范

| 规范项 | 要求 | 示例 |
|--------|------|------|
| 路由前缀 | 业务模块用 `/business/` | `/business/product` |
| 权限标识 | `模块:功能:操作` | `business:product:list` |
| 响应工具 | 统一使用 `ResponseUtil` | `ResponseUtil.success()` |
| 日志记录 | 使用 `@Log` 装饰器 | `@Log(title='产品管理')` |
| 参数验证 | 使用 `@ValidateFields` | `@ValidateFields(...)` |

### 依赖注入规范

```python
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency

async def some_function(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],  # 数据库会话
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],  # 当前用户
) -> Response:
    pass
```

---

## 五、常用工具类

框架提供的工具类，直接使用，禁止修改：

| 工具类 | 用途 | 常用方法 |
|--------|------|----------|
| `ResponseUtil` | 统一响应 | `success(data=...)`, `success(msg=...)` |
| `PageUtil` | 分页查询 | `paginate(db, query, page_num, page_size)` |
| `CamelCaseUtil` | 驼峰转换 | `transform_result(db_obj)` |
| `ExcelUtil` | Excel 导入导出 | `export_excel(...)`, `import_excel(...)` |
| `logger` | 日志记录 | `logger.info(...)`, `logger.error(...)` |

**使用示例：**

```python
# 响应工具
ResponseUtil.success(data=data)
ResponseUtil.success(msg='操作成功')
ResponseUtil.success(model_content=page_result)

# 分页工具
await PageUtil.paginate(db, query, page_num, page_size, is_page)

# 驼峰转换
CamelCaseUtil.transform_result(db_obj)

# 日志记录
logger.info('操作成功')
logger.error('操作失败')
```

---

## 六、数据库表设计规范

### 表命名

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| 系统表 | `sys_[表名]` | `sys_user`, `sys_role` |
| 业务表 | `biz_[表名]` | `biz_product`, `biz_order` |

### 必备字段（审计字段）

每个业务表必须包含以下字段：

```sql
CREATE TABLE `biz_product` (
  `product_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '产品ID',
  `product_name` varchar(100) NOT NULL COMMENT '产品名称',
  -- 其他业务字段...
  
  -- 审计字段（必须）
  `create_by` varchar(64) DEFAULT NULL COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT NULL COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品表';
```

### 实体类定义（DO）

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from config.get_db import Base

class BizProduct(Base):
    __tablename__ = 'biz_product'
    __table_args__ = ({'comment': '产品表'})

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='产品ID')
    product_name: Mapped[str] = mapped_column(String(100), comment='产品名称')
    
    # 审计字段
    create_by: Mapped[str | None] = mapped_column(String(64), comment='创建者')
    create_time: Mapped[datetime | None] = mapped_column(comment='创建时间')
    update_by: Mapped[str | None] = mapped_column(String(64), comment='更新者')
    update_time: Mapped[datetime | None] = mapped_column(comment='更新时间')
    remark: Mapped[str | None] = mapped_column(String(500), comment='备注')
```

---

## 七、菜单和权限配置

### 菜单配置

在系统管理 → 菜单管理中配置：

| 配置项 | 说明 | 示例 |
|--------|------|------|
| 菜单类型 | 目录(M) / 菜单(C) / 按钮(F) | 菜单(C) |
| 菜单名称 | 显示名称 | 产品管理 |
| 路由地址 | 前端路由 | `/business/product` |
| 权限标识 | 后端接口权限 | `business:product:list` |
| 菜单顺序 | 排序号 | 100（业务模块从100开始） |

---

## 八、开发检查清单

提交代码前，请确认：

- [ ] 没有修改框架核心文件（`common/`, `config/`, `utils/`, `middlewares/`, `exceptions/`）
- [ ] 没有修改系统模块（`module_admin/`）
- [ ] 新增模块放在 `module_business/` 目录
- [ ] 文件和类命名符合规范
- [ ] 添加了完整的类型注解
- [ ] 数据库操作包含事务处理（commit/rollback）
- [ ] API 接口添加了权限控制装饰器
- [ ] 使用了统一的响应工具 `ResponseUtil`
- [ ] 添加了适当的日志记录
- [ ] 代码通过 ruff 检查（运行 `ruff check .`）

---

## 九、代码生成器配置

### 配置文件位置

`config/env.py` 中的 `GenSettings` 类：

```python
class GenSettings:
    author = 'insistence'              # 代码作者
    package_name = 'module_business'   # 生成到 module_business 目录
    auto_remove_pre = True             # 自动去除表前缀
    table_prefix = 'sys_,biz_'         # 表前缀识别
    allow_overwrite = True             # 是否允许覆盖本地文件
    GEN_PATH = 'vf_admin/gen_path'     # 生成代码输出路径
```

### 字段类型映射

| 数据库类型 | Python 类型 |
|-----------|-------------|
| `varchar`, `char`, `text` | `str` |
| `int`, `bigint`, `tinyint` | `int` |
| `decimal`, `float`, `double` | `float` |
| `datetime`, `timestamp` | `datetime` |
| `date` | `date` |

### 特殊字段处理

代码生成器会自动识别特殊字段：

| 字段名规则 | 控件类型 |
|-----------|----------|
| 以 `name` 结尾 | 查询方式为 `LIKE` |
| 以 `status` 结尾 | 单选框 |
| 以 `type` 或 `sex` 结尾 | 下拉框 |
| 以 `image` 结尾 | 图片上传 |
| 以 `file` 结尾 | 文件上传 |
| 以 `content` 结尾 | 富文本编辑器 |
| 长度 >= 500 或类型为 `text` | 文本域 |

### 自动排除的字段

- 不在编辑表单显示：`create_by`, `create_time`, `update_by`, `update_time`
- 不在列表显示：`remark`
- 不在查询条件：主键字段

---

## 十、AI 辅助开发建议

使用 AI（如 Kiro）协助开发时：

1. **明确使用代码生成器**
   - "使用代码生成器创建产品管理模块"
   - "参考代码生成器模板创建订单模块"

2. **提供完整表结构**
   - 包含所有字段定义、注释、索引和约束

3. **说明特殊需求**
   - 唯一性校验、主子表关联、树形结构、特殊业务逻辑

4. **参考现有模块**
   - "参考 post_controller.py 的写法"
   - "按照 module_admin 的结构创建"

5. **遵循项目规范**
   - AI 会自动遵循本规则文档
   - 不会修改框架核心文件
   - 保持代码风格一致

---

## 附录：代码模板

### Controller 层模板

```python
from datetime import datetime
from typing import Annotated
from fastapi import Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from common.annotation.log_annotation import Log
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import PageResponseModel, ResponseBaseModel
from module_[业务名].entity.vo.[业务名]_vo import [业务名]Model, [业务名]PageQueryModel
from module_[业务名].service.[业务名]_service import [业务名]Service
from utils.log_util import logger
from utils.response_util import ResponseUtil

[业务名]_controller = APIRouterPro(
    prefix='/business/[业务名]',
    order_num=100,
    tags=['业务管理-[业务名]管理'],
    dependencies=[PreAuthDependency()]
)

@[业务名]_controller.get(
    '/list',
    summary='获取[业务名]分页列表',
    response_model=PageResponseModel[[业务名]Model],
    dependencies=[UserInterfaceAuthDependency('business:[业务名]:list')],
)
async def get_[业务名]_list(
    request: Request,
    query: Annotated[[业务名]PageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await [业务名]Service.get_[业务名]_list_services(query_db, query, is_page=True)
    logger.info('获取成功')
    return ResponseUtil.success(model_content=result)

@[业务名]_controller.post(
    '',
    summary='新增[业务名]',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('business:[业务名]:add')],
)
@Log(title='[业务名]管理', business_type=BusinessType.INSERT)
async def add_[业务名](
    request: Request,
    add_obj: [业务名]Model,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_obj.create_by = current_user.user.user_name
    add_obj.create_time = datetime.now()
    result = await [业务名]Service.add_[业务名]_services(query_db, add_obj)
    return ResponseUtil.success(msg=result.message)
```

### Service 层模板

```python
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from common.vo import CrudResponseModel, PageModel
from module_[业务名].dao.[业务名]_dao import [业务名]Dao
from module_[业务名].entity.vo.[业务名]_vo import [业务名]Model, [业务名]PageQueryModel

class [业务名]Service:
    """[业务名]管理服务层"""

    @classmethod
    async def get_[业务名]_list_services(
        cls, query_db: AsyncSession, query_object: [业务名]PageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """获取[业务名]列表"""
        return await [业务名]Dao.get_[业务名]_list(query_db, query_object, is_page)

    @classmethod
    async def add_[业务名]_services(cls, query_db: AsyncSession, obj: [业务名]Model) -> CrudResponseModel:
        """新增[业务名]"""
        try:
            await [业务名]Dao.add_[业务名]_dao(query_db, obj)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e
```

### DAO 层模板

```python
from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from common.vo import PageModel
from module_[业务名].entity.do.[业务名]_do import [业务名表名]
from module_[业务名].entity.vo.[业务名]_vo import [业务名]Model, [业务名]PageQueryModel
from utils.page_util import PageUtil

class [业务名]Dao:
    """[业务名]管理数据库操作层"""

    @classmethod
    async def get_[业务名]_list(
        cls, db: AsyncSession, query_object: [业务名]PageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """获取[业务名]列表"""
        query = select([业务名表名]).order_by([业务名表名].create_time.desc())
        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def add_[业务名]_dao(cls, db: AsyncSession, obj: [业务名]Model) -> [业务名表名]:
        """新增[业务名]"""
        db_obj = [业务名表名](**obj.model_dump())
        db.add(db_obj)
        await db.flush()
        return db_obj
```

---

## 参考资源

| 资源 | 位置 |
|------|------|
| 项目文档 | `README.md` |
| 代码规范 | `ruff.toml` |
| 示例模块 | `module_admin/controller/post_controller.py` |
| 生成器模板 | `module_generator/templates/python/` |
| API 文档 | 启动后访问 `/docs` |

---

**记住：新增功能，不改框架！业务代码放 `module_business`，保持代码风格一致！**
