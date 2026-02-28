---
inclusion: always
---

# RuoYi-FastAPI 项目开发规则

## 🚨 核心原则：保护框架完整性

### 禁止修改的核心文件和目录

**绝对禁止修改以下文件和目录：**

1. **应用入口和配置**
   - `ruoyi-fastapi-backend/app.py`
   - `ruoyi-fastapi-backend/server.py`
   - `ruoyi-fastapi-backend/config/` 目录下所有文件
   - `ruoyi-fastapi-backend/alembic/` 目录（数据库迁移）
   - `ruoyi-fastapi-backend/alembic.ini`

2. **框架核心模块**
   - `ruoyi-fastapi-backend/common/` 目录（公共组件）
   - `ruoyi-fastapi-backend/exceptions/` 目录（异常处理）
   - `ruoyi-fastapi-backend/middlewares/` 目录（中间件）
   - `ruoyi-fastapi-backend/utils/` 目录（工具类）
   - `ruoyi-fastapi-backend/sub_applications/` 目录（子应用）

3. **系统管理模块（除非明确需求）**
   - `ruoyi-fastapi-backend/module_admin/` 目录
   - 包括用户、角色、菜单、部门、岗位、字典、参数、日志等核心功能

4. **其他核心模块**
   - `ruoyi-fastapi-backend/module_task/` 目录（定时任务）
   - `ruoyi-fastapi-backend/module_generator/` 目录（代码生成器）

5. **Docker 和环境配置**
   - `docker-compose.*.yml`
   - `Dockerfile.*`
   - `.env.*` 文件（可以修改配置值，但不要删除或重命名）

---

## ✅ 新增功能的标准流程

### 1. 创建新模块（推荐方式）

新增业务功能时，应创建独立的业务模块，遵循以下目录结构：

```
ruoyi-fastapi-backend/
└── module_[业务名称]/          # 例如：module_product, module_order
    ├── controller/              # 控制器层（API接口）
    │   └── [业务]_controller.py
    ├── service/                 # 服务层（业务逻辑）
    │   └── [业务]_service.py
    ├── dao/                     # 数据访问层（数据库操作）
    │   └── [业务]_dao.py
    └── entity/                  # 实体层
        ├── do/                  # 数据库实体（Database Object）
        │   └── [业务]_do.py
        └── vo/                  # 视图对象（View Object）
            └── [业务]_vo.py
```

### 2. 命名规范

**文件命名：**
- Controller: `[业务名]_controller.py`
- Service: `[业务名]_service.py`
- DAO: `[业务名]_dao.py`
- DO: `[业务名]_do.py`
- VO: `[业务名]_vo.py`

**类命名：**
- Controller: `[业务名首字母大写]Controller` 类不需要，直接定义路由对象
- Service: `[业务名首字母大写]Service`
- DAO: `[业务名首字母大写]Dao`
- DO: `Sys[业务名首字母大写]` 或 `[业务名首字母大写]`
- VO: `[业务名首字母大写]Model`, `[业务名首字母大写]PageQueryModel`

**路由对象命名：**
```python
# 使用 APIRouterPro，命名格式：[业务名]_controller
product_controller = APIRouterPro(
    prefix='/business/product',
    order_num=100,  # 自定义排序号，避免与系统模块冲突（系统模块使用1-20）
    tags=['业务管理-产品管理'],
    dependencies=[PreAuthDependency()]
)
```

### 3. 代码结构模板

#### Controller 层模板

```python
from datetime import datetime
from typing import Annotated

from fastapi import Form, Path, Query, Request, Response
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.log_annotation import Log
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
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
    summary='获取[业务名]分页列表接口',
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
    summary='新增[业务名]接口',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('business:[业务名]:add')],
)
@ValidateFields(validate_model='add_[业务名]')
@Log(title='[业务名]管理', business_type=BusinessType.INSERT)
async def add_[业务名](
    request: Request,
    add_obj: [业务名]Model,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_obj.create_by = current_user.user.user_name
    add_obj.create_time = datetime.now()
    add_obj.update_by = current_user.user.user_name
    add_obj.update_time = datetime.now()
    result = await [业务名]Service.add_[业务名]_services(query_db, add_obj)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)
```

#### Service 层模板

```python
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_[业务名].dao.[业务名]_dao import [业务名]Dao
from module_[业务名].entity.vo.[业务名]_vo import [业务名]Model, [业务名]PageQueryModel
from utils.common_util import CamelCaseUtil


class [业务名]Service:
    """
    [业务名]管理模块服务层
    """

    @classmethod
    async def get_[业务名]_list_services(
        cls, query_db: AsyncSession, query_object: [业务名]PageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取[业务名]列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: [业务名]列表信息对象
        """
        result = await [业务名]Dao.get_[业务名]_list(query_db, query_object, is_page)
        return result

    @classmethod
    async def add_[业务名]_services(cls, query_db: AsyncSession, obj: [业务名]Model) -> CrudResponseModel:
        """
        新增[业务名]信息service

        :param query_db: orm对象
        :param obj: 新增[业务名]对象
        :return: 新增[业务名]校验结果
        """
        try:
            await [业务名]Dao.add_[业务名]_dao(query_db, obj)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def [业务名]_detail_services(cls, query_db: AsyncSession, id: int) -> [业务名]Model:
        """
        获取[业务名]详细信息service

        :param query_db: orm对象
        :param id: [业务名]id
        :return: [业务名]详细信息
        """
        obj = await [业务名]Dao.get_[业务名]_detail_by_id(query_db, id=id)
        result = [业务名]Model(**CamelCaseUtil.transform_result(obj)) if obj else [业务名]Model()
        return result
```

#### DAO 层模板

```python
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_[业务名].entity.do.[业务名]_do import [业务名表名]
from module_[业务名].entity.vo.[业务名]_vo import [业务名]Model, [业务名]PageQueryModel
from utils.page_util import PageUtil


class [业务名]Dao:
    """
    [业务名]管理模块数据库操作层
    """

    @classmethod
    async def get_[业务名]_detail_by_id(cls, db: AsyncSession, id: int) -> [业务名表名] | None:
        """
        根据id获取[业务名]详细信息

        :param db: orm对象
        :param id: [业务名]id
        :return: [业务名]信息对象
        """
        obj = (await db.execute(select([业务名表名]).where([业务名表名].id == id))).scalars().first()
        return obj

    @classmethod
    async def get_[业务名]_list(
        cls, db: AsyncSession, query_object: [业务名]PageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取[业务名]列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: [业务名]列表信息对象
        """
        query = select([业务名表名]).where(
            # 添加查询条件
        ).order_by([业务名表名].create_time.desc()).distinct()
        
        result: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )
        return result

    @classmethod
    async def add_[业务名]_dao(cls, db: AsyncSession, obj: [业务名]Model) -> [业务名表名]:
        """
        新增[业务名]数据库操作

        :param db: orm对象
        :param obj: [业务名]对象
        :return: 新增的[业务名]对象
        """
        db_obj = [业务名表名](**obj.model_dump())
        db.add(db_obj)
        await db.flush()
        return db_obj
```

---

## 📋 代码规范要求

### 1. Python 代码规范

遵循项目的 `ruff.toml` 配置：

- **行长度限制**: 120字符
- **Python版本**: >= 3.10
- **引号风格**: 单引号 `'`
- **类型注解**: 必须添加函数参数和返回值的类型注解
- **导入顺序**: 使用 isort 自动排序
- **命名规范**:
  - 类名: PascalCase（大驼峰）
  - 函数名: snake_case（下划线）
  - 常量: UPPER_CASE（全大写）
  - 变量: snake_case（下划线）

### 2. 数据库操作规范

- **必须使用事务**: 所有写操作（增删改）必须包含 `commit` 和 `rollback`
- **异常处理**: 使用 `try-except` 捕获异常并回滚事务
- **查询优化**: 使用 `select().where()` 而不是 `filter()`
- **分页查询**: 使用 `PageUtil.paginate()` 工具方法

```python
try:
    await SomeDao.add_something(query_db, obj)
    await query_db.commit()
    return CrudResponseModel(is_success=True, message='操作成功')
except Exception as e:
    await query_db.rollback()
    raise e
```

### 3. API 接口规范

- **路由前缀**: 业务模块使用 `/business/[模块名]`，系统模块使用 `/system/[模块名]`
- **权限标识**: 格式为 `模块:功能:操作`，例如 `business:product:list`
- **响应模型**: 统一使用 `ResponseUtil` 返回
  - 列表: `PageResponseModel`
  - 详情: `DataResponseModel`
  - 操作: `ResponseBaseModel`
- **日志记录**: 使用 `@Log` 装饰器记录操作日志
- **参数验证**: 使用 `@ValidateFields` 装饰器验证参数

### 4. 依赖注入规范

统一使用框架提供的依赖注入：

```python
from typing import Annotated
from fastapi import Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.pre_auth import CurrentUserDependency
from module_admin.entity.vo.user_vo import CurrentUserModel

async def some_function(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    pass
```

---

## 🔧 工具类使用规范

### 只使用，不修改

框架提供了丰富的工具类，直接使用即可，禁止修改：

- `ResponseUtil`: 统一响应工具
- `PageUtil`: 分页工具
- `CamelCaseUtil`: 驼峰转换工具
- `ExcelUtil`: Excel导入导出工具
- `logger`: 日志工具（来自 `utils.log_util`）

### 常用工具方法

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

## 🎯 权限和菜单配置

### 1. 菜单配置

新增功能需要在系统管理-菜单管理中配置：

- **菜单类型**: 目录(M) / 菜单(C) / 按钮(F)
- **路由地址**: 前端路由路径
- **权限标识**: 对应后端接口的权限标识
- **菜单顺序**: 自定义排序号（建议从100开始）

### 2. 权限标识规范

格式：`模块:功能:操作`

示例：
- `business:product:list` - 产品列表查询
- `business:product:add` - 产品新增
- `business:product:edit` - 产品编辑
- `business:product:remove` - 产品删除
- `business:product:export` - 产品导出

---

## 📦 数据库表设计规范

### 1. 表命名

- 系统表: `sys_[表名]`
- 业务表: `biz_[表名]` 或直接 `[表名]`

### 2. 必备字段

每个业务表应包含以下审计字段：

```python
create_by: str | None = None      # 创建者
create_time: datetime | None = None  # 创建时间
update_by: str | None = None      # 更新者
update_time: datetime | None = None  # 更新时间
remark: str | None = None         # 备注
```

### 3. 实体类定义（DO）

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from config.get_db import Base

class BizProduct(Base):
    __tablename__ = 'biz_product'
    __table_args__ = ({'comment': '产品表'})

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='产品ID')
    product_name: Mapped[str] = mapped_column(String(100), comment='产品名称')
    # ... 其他字段
    create_by: Mapped[str | None] = mapped_column(String(64), comment='创建者')
    create_time: Mapped[datetime | None] = mapped_column(comment='创建时间')
```

---

## ⚠️ 特别注意事项

### 1. 不要修改框架的路由注册机制

框架使用 `auto_register_routers()` 自动注册路由，不要手动修改 `server.py` 中的路由注册逻辑。

### 2. 不要修改中间件和异常处理

框架已配置好中间件和全局异常处理，不要修改：
- `middlewares/handle.py`
- `exceptions/handle.py`

### 3. 不要修改数据库连接配置

数据库连接由 `config/get_db.py` 管理，不要修改连接逻辑，只修改 `.env.*` 文件中的配置值。

### 4. 不要修改 Redis 配置

Redis 连接由 `config/get_redis.py` 管理，不要修改连接逻辑。

### 5. 使用代码生成器（强烈推荐）

对于标准的 CRUD 功能，优先使用系统自带的代码生成器：
- 访问：系统工具 -> 代码生成
- 配置数据库表信息
- 一键生成前后端代码

代码生成器会自动生成：
- Controller 层（API 接口）
- Service 层（业务逻辑）
- DAO 层（数据库操作）
- DO 层（数据库实体）
- VO 层（视图对象）
- 前端 Vue 页面和 API 文件

生成的代码完全符合框架规范，包括：
- 统一的命名规范
- 完整的类型注解
- 事务处理
- 权限控制
- 日志记录
- 参数验证
- Excel 导出功能

---

## 📝 开发检查清单

在提交代码前，请确认：

- [ ] 没有修改框架核心文件（`common/`, `config/`, `utils/`, `middlewares/`, `exceptions/`）
- [ ] 没有修改系统管理模块（`module_admin/`），除非有明确需求
- [ ] 新增模块遵循标准目录结构（controller/service/dao/entity）
- [ ] 文件和类命名符合规范
- [ ] 添加了完整的类型注解
- [ ] 数据库操作包含事务处理（commit/rollback）
- [ ] API 接口添加了权限控制装饰器
- [ ] 使用了统一的响应工具 `ResponseUtil`
- [ ] 添加了适当的日志记录
- [ ] 代码通过 ruff 检查（运行 `ruff check .`）

---

## 🚀 快速开始新功能

### 方式一：使用代码生成器（推荐）

1. **创建数据库表**
   ```sql
   CREATE TABLE `biz_product` (
     `product_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '产品ID',
     `product_name` varchar(100) NOT NULL COMMENT '产品名称',
     `product_code` varchar(50) DEFAULT NULL COMMENT '产品编码',
     `status` char(1) DEFAULT '0' COMMENT '状态（0正常 1停用）',
     `create_by` varchar(64) DEFAULT NULL COMMENT '创建者',
     `create_time` datetime DEFAULT NULL COMMENT '创建时间',
     `update_by` varchar(64) DEFAULT NULL COMMENT '更新者',
     `update_time` datetime DEFAULT NULL COMMENT '更新时间',
     `remark` varchar(500) DEFAULT NULL COMMENT '备注',
     PRIMARY KEY (`product_id`)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品表';
   ```

2. **导入表到代码生成器**
   - 登录系统管理后台
   - 访问：系统工具 -> 代码生成
   - 点击"导入"按钮，选择刚创建的表
   - 点击"编辑"配置生成信息：
     - 基本信息：模块名、业务名、功能名、作者
     - 生成信息：生成路径、包路径
     - 字段信息：配置每个字段的显示类型、查询方式等

3. **生成代码**
   - 点击"生成代码"按钮下载代码包
   - 或点击"生成代码（本地）"直接生成到项目目录

4. **配置菜单和权限**
   - 在菜单管理中添加新菜单
   - 配置权限标识（如：`business:product:list`）

5. **测试功能**
   - 重启后端服务
   - 访问 Swagger 文档测试接口
   - 在前端页面测试完整流程

### 方式二：手动创建模块

1. **创建模块目录**
   ```bash
   cd ruoyi-fastapi-backend
   mkdir -p module_[业务名]/{controller,service,dao,entity/{do,vo}}
   ```

2. **创建基础文件**
   - `controller/[业务名]_controller.py`
   - `service/[业务名]_service.py`
   - `dao/[业务名]_dao.py`
   - `entity/do/[业务名]_do.py`
   - `entity/vo/[业务名]_vo.py`

3. **参考模板编写代码**
   - 参考 `module_admin/controller/post_controller.py` 等文件
   - 或参考代码生成器的模板文件：`module_generator/templates/python/`
   - 复制模板代码并修改业务逻辑

4. **配置菜单和权限**
   - 登录系统管理后台
   - 在菜单管理中添加新菜单
   - 配置权限标识

5. **测试功能**
   - 访问 Swagger 文档测试接口
   - 在前端页面测试完整流程

### 代码生成器的优势

- ✅ 自动生成符合框架规范的代码
- ✅ 包含完整的 CRUD 功能
- ✅ 自动配置权限控制和日志记录
- ✅ 支持 Excel 导出功能
- ✅ 支持字段唯一性校验
- ✅ 支持主子表关联
- ✅ 支持树形结构
- ✅ 节省大量开发时间

---

## 📚 参考资源

- 项目文档: `README.md`
- 代码规范: `ruff.toml`
- 示例模块: `module_admin/controller/post_controller.py`
- 代码生成器模板: `module_generator/templates/python/`
- 代码生成工具类: `utils/gen_util.py`
- API 文档: 启动后访问 `/docs`

---

## 🎨 代码生成器配置说明

### 生成器模板位置

- Python 后端模板: `module_generator/templates/python/`
  - `controller.py.jinja2` - Controller 层模板
  - `service.py.jinja2` - Service 层模板
  - `dao.py.jinja2` - DAO 层模板
  - `do.py.jinja2` - DO 实体模板
  - `vo.py.jinja2` - VO 对象模板

- 前端模板: `module_generator/templates/vue/` 和 `module_generator/templates/js/`

### 生成器配置项

在 `config/env.py` 中的 `GenConfig` 类配置：

```python
class GenConfig:
    author = '作者名'  # 代码作者
    package_name = 'module_业务'  # 包名
    auto_remove_pre = True  # 是否自动去除表前缀
    table_prefix = 'sys_,biz_'  # 表前缀（多个用逗号分隔）
    GEN_PATH = 'gen_code'  # 生成代码的输出路径
    allow_overwrite = False  # 是否允许覆盖本地文件（生产环境建议关闭）
```

### 字段类型映射

代码生成器会自动将数据库字段类型映射为 Python 类型：

- `varchar`, `char`, `text` → `str`
- `int`, `bigint`, `tinyint` → `int`
- `decimal`, `float`, `double` → `float`
- `datetime`, `timestamp` → `datetime`
- `date` → `date`

### 字段命名规则

- 数据库字段：`snake_case`（下划线命名）
- Python 字段：`camelCase`（小驼峰）
- 类名：`PascalCase`（大驼峰）

示例：
- 数据库字段：`product_name`
- Python 字段：`productName`
- 类名：`ProductModel`

### 特殊字段处理

代码生成器会自动识别特殊字段并配置相应的控件：

- 字段名以 `name` 结尾 → 查询方式为 `LIKE`
- 字段名以 `status` 结尾 → 显示为单选框
- 字段名以 `type` 或 `sex` 结尾 → 显示为下拉框
- 字段名以 `image` 结尾 → 显示为图片上传控件
- 字段名以 `file` 结尾 → 显示为文件上传控件
- 字段名以 `content` 结尾 → 显示为富文本编辑器
- 字段长度 >= 500 或类型为 `text` → 显示为文本域

### 自动排除的字段

以下字段会被自动排除在某些操作之外：

- 不在编辑表单显示：`create_by`, `create_time`, `update_by`, `update_time`
- 不在列表显示：`remark`（备注字段）
- 不在查询条件：主键字段

---

## 💡 AI 辅助开发建议

当使用 AI（如 Kiro）协助开发时：

1. **明确告知使用代码生成器**
   - "请使用代码生成器创建产品管理模块"
   - "参考代码生成器的模板创建订单模块"

2. **提供完整的表结构**
   - 包含所有字段定义
   - 包含字段注释
   - 包含索引和约束

3. **说明特殊需求**
   - 是否需要唯一性校验
   - 是否需要主子表关联
   - 是否需要树形结构
   - 特殊的业务逻辑

4. **参考现有模块**
   - "参考 post_controller.py 的写法"
   - "按照 module_admin 的结构创建"

5. **遵循项目规范**
   - AI 会自动遵循 `.kiro/steering/project-development-rules.md` 中的规则
   - 不会修改框架核心文件
   - 保持代码风格一致

---

**记住：新增功能，不改框架！保持代码风格一致，遵循项目规范！**
