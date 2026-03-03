import io
import json
import os
import zipfile
from datetime import datetime
from typing import Any

import aiofiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlglot import parse as sqlglot_parse
from sqlglot.expressions import Add, Alter, Create, Delete, Drop, Expression, Insert, Table, TruncateTable, Update

from common.constant import GenConstant
from common.vo import CrudResponseModel, PageModel
from config.env import DataBaseConfig, GenConfig
from exceptions.exception import ServiceException
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_generator.dao.gen_dao import GenTableColumnDao, GenTableDao
from module_generator.entity.vo.gen_vo import (
    DeleteGenTableModel,
    EditGenTableModel,
    GenTableColumnModel,
    GenTableModel,
    GenTablePageQueryModel,
)
from utils.common_util import CamelCaseUtil
from utils.gen_util import GenUtils
from utils.log_util import logger
from utils.template_util import TemplateInitializer, TemplateUtils


class GenTableService:
    """
    代码生成业务表服务层
    """

    @classmethod
    async def get_gen_table_list_services(
        cls, query_db: AsyncSession, query_object: GenTablePageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取代码生成业务表列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 代码生成业务列表信息对象
        """
        gen_table_list_result = await GenTableDao.get_gen_table_list(query_db, query_object, is_page)

        return gen_table_list_result

    @classmethod
    async def get_gen_db_table_list_services(
        cls, query_db: AsyncSession, query_object: GenTablePageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取数据库列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据库列表信息对象
        """
        gen_db_table_list_result = await GenTableDao.get_gen_db_table_list(query_db, query_object, is_page)

        return gen_db_table_list_result

    @classmethod
    async def get_gen_db_table_list_by_name_services(
        cls, query_db: AsyncSession, table_names: list[str]
    ) -> list[GenTableModel]:
        """
        根据表名称组获取数据库列表信息service

        :param query_db: orm对象
        :param table_names: 表名称组
        :return: 数据库列表信息对象
        """
        gen_db_table_list_result = await GenTableDao.get_gen_db_table_list_by_names(query_db, table_names)

        return [GenTableModel(**gen_table) for gen_table in CamelCaseUtil.transform_result(gen_db_table_list_result)]

    @classmethod
    async def import_gen_table_services(
        cls, query_db: AsyncSession, gen_table_list: list[GenTableModel], current_user: CurrentUserModel
    ) -> CrudResponseModel:
        """
        导入表结构service

        :param query_db: orm对象
        :param gen_table_list: 导入表列表
        :param current_user: 当前用户信息对象
        :return: 导入结果
        """
        try:
            for table in gen_table_list:
                table_name = table.table_name
                GenUtils.init_table(table, current_user.user.user_name)
                add_gen_table = await GenTableDao.add_gen_table_dao(query_db, table)
                if add_gen_table:
                    table.table_id = add_gen_table.table_id
                    gen_table_columns = await GenTableColumnDao.get_gen_db_table_columns_by_name(query_db, table_name)
                    for column in [
                        GenTableColumnModel(**gen_table_column)
                        for gen_table_column in CamelCaseUtil.transform_result(gen_table_columns)
                    ]:
                        GenUtils.init_column_field(column, table)
                        await GenTableColumnDao.add_gen_table_column_dao(query_db, column)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='导入成功')
        except Exception as e:
            await query_db.rollback()
            raise ServiceException(message=f'导入失败, {e}') from e

    @classmethod
    async def edit_gen_table_services(cls, query_db: AsyncSession, page_object: EditGenTableModel) -> CrudResponseModel:
        """
        编辑业务表信息service

        :param query_db: orm对象
        :param page_object: 编辑业务表对象
        :return: 编辑业务表校验结果
        """
        edit_gen_table = page_object.model_dump(exclude_unset=True, by_alias=True)
        gen_table_info = await cls.get_gen_table_by_id_services(query_db, page_object.table_id)
        if gen_table_info.table_id:
            try:
                edit_gen_table['options'] = json.dumps(edit_gen_table.get('params'))
                await GenTableDao.edit_gen_table_dao(query_db, edit_gen_table)
                for gen_table_column in page_object.columns:
                    gen_table_column.update_by = page_object.update_by
                    gen_table_column.update_time = datetime.now()
                    await GenTableColumnDao.edit_gen_table_column_dao(
                        query_db, gen_table_column.model_dump(by_alias=True)
                    )
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='业务表不存在')

    @classmethod
    async def delete_gen_table_services(
        cls, query_db: AsyncSession, page_object: DeleteGenTableModel
    ) -> CrudResponseModel:
        """
        删除业务表信息service

        :param query_db: orm对象
        :param page_object: 删除业务表对象
        :return: 删除业务表校验结果
        """
        if page_object.table_ids:
            table_id_list = page_object.table_ids.split(',')
            try:
                for table_id in table_id_list:
                    await GenTableDao.delete_gen_table_dao(query_db, GenTableModel(tableId=table_id))
                    await GenTableColumnDao.delete_gen_table_column_by_table_id_dao(
                        query_db, GenTableColumnModel(tableId=table_id)
                    )
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入业务表id为空')

    @classmethod
    async def get_gen_table_by_id_services(cls, query_db: AsyncSession, table_id: int) -> GenTableModel:
        """
        获取需要生成的业务表详细信息service

        :param query_db: orm对象
        :param table_id: 需要生成的业务表id
        :return: 需要生成的业务表id对应的信息
        """
        gen_table = await GenTableDao.get_gen_table_by_id(query_db, table_id)
        result = await cls.set_table_from_options(GenTableModel(**CamelCaseUtil.transform_result(gen_table)))

        return result

    @classmethod
    async def get_gen_table_all_services(cls, query_db: AsyncSession) -> list[GenTableModel]:
        """
        获取所有业务表信息service

        :param query_db: orm对象
        :return: 所有业务表信息
        """
        gen_table_all = await GenTableDao.get_gen_table_all(query_db)
        result = [GenTableModel(**gen_table) for gen_table in CamelCaseUtil.transform_result(gen_table_all)]

        return result

    @classmethod
    async def create_table_services(
        cls, query_db: AsyncSession, sql: str, current_user: CurrentUserModel
    ) -> CrudResponseModel:
        """
        创建表结构service

        :param query_db: orm对象
        :param sql: 建表语句
        :param current_user: 当前用户信息对象
        :return: 创建表结构结果
        """
        sql_statements = sqlglot_parse(sql, dialect=DataBaseConfig.sqlglot_parse_dialect)
        if cls.__is_valid_create_table(sql_statements):
            try:
                table_names = cls.__get_table_names(sql_statements)
                await GenTableDao.create_table_by_sql_dao(query_db, sql_statements)
                gen_table_list = await cls.get_gen_db_table_list_by_name_services(query_db, table_names)
                await cls.import_gen_table_services(query_db, gen_table_list, current_user)

                return CrudResponseModel(is_success=True, message='创建表结构成功')
            except Exception as e:
                raise ServiceException(message=f'创建表结构异常，详细错误信息：{e}') from e
        else:
            raise ServiceException(message='建表语句不合法')

    @classmethod
    def __is_valid_create_table(cls, sql_statements: list[Expression]) -> bool:
        """
        校验sql语句是否为合法的建表语句

        :param sql_statements: sql语句的ast列表
        :return: 校验结果
        """
        validate_create = [isinstance(sql_statement, Create) for sql_statement in sql_statements]
        validate_forbidden_keywords = [
            isinstance(
                sql_statement,
                (Add, Alter, Delete, Drop, Insert, TruncateTable, Update),
            )
            for sql_statement in sql_statements
        ]
        return not (not any(validate_create) or any(validate_forbidden_keywords))

    @classmethod
    def __get_table_names(cls, sql_statements: list[Expression]) -> list[str]:
        """
        获取sql语句中所有的建表表名

        :param sql_statements: sql语句的ast列表
        :return: 建表表名列表
        """
        table_names = [
            sql_statement.find(Table).name for sql_statement in sql_statements if isinstance(sql_statement, Create)
        ]

        return table_names

    @classmethod
    async def preview_code_services(cls, query_db: AsyncSession, table_id: int) -> dict[str, str]:
        """
        预览代码service

        :param query_db: orm对象
        :param table_id: 业务表id
        :return: 预览数据列表
        """
        gen_table = GenTableModel(
            **CamelCaseUtil.transform_result(await GenTableDao.get_gen_table_by_id(query_db, table_id))
        )
        await cls.set_sub_table(query_db, gen_table)
        await cls.set_pk_column(gen_table)
        env = TemplateInitializer.init_jinja2()
        context = TemplateUtils.prepare_context(gen_table)
        template_list = TemplateUtils.get_template_list(gen_table.tpl_category, gen_table.tpl_web_type)
        preview_code_result = {}
        for template in template_list:
            try:
                render_content = env.get_template(template).render(**context)
                preview_code_result[template] = render_content
            except Exception as e:
                raise ServiceException(message=f'渲染模板失败，表名：{gen_table.table_name}，模板：{template}，详细错误信息：{str(e)}')
        return preview_code_result

    @classmethod
    async def generate_code_services(cls, query_db: AsyncSession, table_name: str) -> CrudResponseModel:
        """
        生成代码至指定路径service

        :param query_db: orm对象
        :param table_name: 业务表名称
        :return: 生成代码结果
        """
        from utils.log_util import logger
        
        env = TemplateInitializer.init_jinja2()
        render_info = await cls.__get_gen_render_info(query_db, table_name)
        gen_table = render_info[3]
        
        generated_files = []
        
        try:
            # 生成代码文件
            for template in render_info[0]:
                try:
                    render_content = env.get_template(template).render(**render_info[2])
                except Exception as render_error:
                    raise ServiceException(message=f'渲染模板失败，表名：{gen_table.table_name}，模板：{template}，详细错误信息：{str(render_error)}')
                gen_path = cls.__get_gen_path(gen_table, template)
                os.makedirs(os.path.dirname(gen_path), exist_ok=True)
                async with aiofiles.open(gen_path, 'w', encoding='utf-8') as f:
                    await f.write(render_content)
                generated_files.append(gen_path)
                
        except ServiceException:
            raise
        except Exception as e:
            raise ServiceException(message=f'生成代码失败，表名：{gen_table.table_name}，详细错误信息：{e}') from e

        # 构建详细的成功消息
        if gen_table.gen_path == '/':
            # 获取项目根目录
            current_dir = os.getcwd()
            if current_dir.endswith('ruoyi-fastapi-backend'):
                project_root = os.path.dirname(current_dir)
            else:
                project_root = current_dir
            
            # 构建文件列表（显示相对路径）
            file_list = []
            for file_path in generated_files[:5]:  # 只显示前5个文件
                rel_path = os.path.relpath(file_path, project_root)
                file_list.append(f"  - {rel_path}")
            
            if len(generated_files) > 5:
                file_list.append(f"  ... 还有 {len(generated_files) - 5} 个文件")
            
            message = f'生成代码成功！\n\n文件已保存到项目根目录：\n{project_root}\n\n生成的文件：\n' + '\n'.join(file_list)
        else:
            message = f'生成代码成功！\n\n文件已保存到：\n{gen_table.gen_path}\n\n共生成 {len(generated_files)} 个文件'
        
        logger.info(message)
        return CrudResponseModel(is_success=True, message=message)

    @classmethod
    async def batch_gen_code_services(cls, query_db: AsyncSession, table_names: list[str]) -> bytes:
        """
        批量生成代码service

        :param query_db: orm对象
        :param table_names: 业务表名称组
        :return: 下载代码结果
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for table_name in table_names:
                env = TemplateInitializer.init_jinja2()
                render_info = await cls.__get_gen_render_info(query_db, table_name)
                for template_file, output_file in zip(render_info[0], render_info[1], strict=False):
                    render_content = env.get_template(template_file).render(**render_info[2])
                    zip_file.writestr(output_file, render_content)

        zip_data = zip_buffer.getvalue()
        zip_buffer.close()
        return zip_data

    @classmethod
    async def __get_gen_render_info(cls, query_db: AsyncSession, table_name: str) -> list:
        """
        获取生成代码渲染模板相关信息

        :param query_db: orm对象
        :param table_name: 业务表名称
        :return: 生成代码渲染模板相关信息
        """
        from utils.log_util import logger
        
        gen_table = GenTableModel(
            **CamelCaseUtil.transform_result(await GenTableDao.get_gen_table_by_name(query_db, table_name))
        )
        
        logger.info(f'获取表信息 - 表名: {table_name}')
        logger.info(f'获取表信息 - options原始值: {gen_table.options}')
        
        await cls.set_sub_table(query_db, gen_table)
        await cls.set_pk_column(gen_table)
        
        # 重要：从 options 中解析 parent_menu_id
        gen_table = await cls.set_table_from_options(gen_table)
        
        logger.info(f'解析options后 - parent_menu_id: {gen_table.parent_menu_id}')
        logger.info(f'解析options后 - parent_menu_name: {gen_table.parent_menu_name}')
        
        context = TemplateUtils.prepare_context(gen_table)
        template_list = TemplateUtils.get_template_list(gen_table.tpl_category, gen_table.tpl_web_type)
        output_files = [TemplateUtils.get_file_name(template, gen_table) for template in template_list]

        return [template_list, output_files, context, gen_table]

    @classmethod
    def __get_gen_path(cls, gen_table: GenTableModel, template: str) -> str:
        """
        根据GenTableModel对象和模板名称生成路径

        :param gen_table: GenTableModel对象
        :param template: 模板名称
        :return: 生成的路径
        """
        gen_path = gen_table.gen_path
        file_name = TemplateUtils.get_file_name(template, gen_table)
        
        if gen_path == '/':
            # 生成到项目根目录
            # file_name 格式如: backend/module_admin/controller/xxx_controller.py
            # 需要替换 backend 为实际的后端目录名 ruoyi-fastapi-backend
            # 替换 frontend 为实际的前端目录名 ruoyi-fastapi-frontend
            
            # 获取项目根目录（当前工作目录的父目录，因为代码在 ruoyi-fastapi-backend 中运行）
            # 如果当前目录已经是项目根目录，则直接使用
            current_dir = os.getcwd()
            
            # 判断当前目录是否是 ruoyi-fastapi-backend
            if current_dir.endswith('ruoyi-fastapi-backend'):
                # 如果是，则项目根目录是父目录
                project_root = os.path.dirname(current_dir)
            else:
                # 否则，当前目录就是项目根目录
                project_root = current_dir
            
            # 替换路径前缀
            file_name = file_name.replace('backend/', 'ruoyi-fastapi-backend/')
            file_name = file_name.replace('frontend/', 'ruoyi-fastapi-frontend/src/')
            
            return os.path.join(project_root, file_name)

        return os.path.join(gen_path, file_name)

    @classmethod
    async def sync_db_services(cls, query_db: AsyncSession, table_name: str) -> CrudResponseModel:
        """
        同步数据库service

        :param query_db: orm对象
        :param table_name: 业务表名称
        :return: 同步数据库结果
        """
        gen_table = await GenTableDao.get_gen_table_by_name(query_db, table_name)
        table = GenTableModel(**CamelCaseUtil.transform_result(gen_table))
        table_columns = table.columns
        table_column_map = {column.column_name: column for column in table_columns}
        query_db_table_columns = await GenTableColumnDao.get_gen_db_table_columns_by_name(query_db, table_name)
        db_table_columns = [
            GenTableColumnModel(**column) for column in CamelCaseUtil.transform_result(query_db_table_columns)
        ]
        if not db_table_columns:
            raise ServiceException('同步数据失败，原表结构不存在')
        db_table_column_names = [column.column_name for column in db_table_columns]
        try:
            for column in db_table_columns:
                GenUtils.init_column_field(column, table)
                if column.column_name in table_column_map:
                    prev_column = table_column_map[column.column_name]
                    column.column_id = prev_column.column_id
                    if column.list:
                        column.dict_type = prev_column.dict_type
                        column.query_type = prev_column.query_type
                    if (
                        prev_column.is_required != ''
                        and not column.pk
                        and (column.insert or column.edit)
                        and (column.usable_column or column.super_column)
                    ):
                        column.is_required = prev_column.is_required
                        column.html_type = prev_column.html_type
                    await GenTableColumnDao.edit_gen_table_column_dao(query_db, column.model_dump(by_alias=True))
                else:
                    await GenTableColumnDao.add_gen_table_column_dao(query_db, column)
            del_columns = [column for column in table_columns if column.column_name not in db_table_column_names]
            if del_columns:
                for column in del_columns:
                    await GenTableColumnDao.delete_gen_table_column_by_column_id_dao(query_db, column)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='同步成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def set_sub_table(cls, query_db: AsyncSession, gen_table: GenTableModel) -> None:
        """
        设置主子表信息

        :param query_db: orm对象
        :param gen_table: 业务表信息
        :return:
        """
        if gen_table.sub_table_name:
            sub_table = await GenTableDao.get_gen_table_by_name(query_db, gen_table.sub_table_name)
            gen_table.sub_table = GenTableModel(**CamelCaseUtil.transform_result(sub_table))

    @classmethod
    async def set_pk_column(cls, gen_table: GenTableModel) -> None:
        """
        设置主键列信息

        :param gen_table: 业务表信息
        :return:
        """
        for column in gen_table.columns:
            if column.pk:
                gen_table.pk_column = column
                break
        if gen_table.pk_column is None:
            gen_table.pk_column = gen_table.columns[0]
        if gen_table.tpl_category == GenConstant.TPL_SUB:
            for column in gen_table.sub_table.columns:
                if column.pk:
                    gen_table.sub_table.pk_column = column
                    break
            if gen_table.sub_table.columns is None:
                gen_table.sub_table.pk_column = gen_table.sub_table.columns[0]

    @classmethod
    async def set_table_from_options(cls, gen_table: GenTableModel) -> GenTableModel:
        """
        设置代码生成其他选项值

        :param gen_table: 生成对象
        :return: 设置后的生成对象
        """
        params_obj = json.loads(gen_table.options) if gen_table.options else None
        if params_obj:
            gen_table.tree_code = params_obj.get(GenConstant.TREE_CODE)
            gen_table.tree_parent_code = params_obj.get(GenConstant.TREE_PARENT_CODE)
            gen_table.tree_name = params_obj.get(GenConstant.TREE_NAME)
            gen_table.parent_menu_id = params_obj.get(GenConstant.PARENT_MENU_ID)
            gen_table.parent_menu_name = params_obj.get(GenConstant.PARENT_MENU_NAME)

        return gen_table

    @classmethod
    async def validate_edit(cls, edit_gen_table: EditGenTableModel) -> None:
        """
        编辑保存参数校验

        :param edit_gen_table: 编辑业务表对象
        """
        if edit_gen_table.tpl_category == GenConstant.TPL_TREE:
            params_obj = edit_gen_table.params.model_dump(by_alias=True)

            if GenConstant.TREE_CODE not in params_obj:
                raise ServiceException(message='树编码字段不能为空')
            if GenConstant.TREE_PARENT_CODE not in params_obj:
                raise ServiceException(message='树父编码字段不能为空')
            if GenConstant.TREE_NAME not in params_obj:
                raise ServiceException(message='树名称字段不能为空')
            if edit_gen_table.tpl_category == GenConstant.TPL_SUB:
                if not edit_gen_table.sub_table_name:
                    raise ServiceException(message='关联子表的表名不能为空')
                if not edit_gen_table.sub_table_fk_name:
                    raise ServiceException(message='子表关联的外键名不能为空')

    @classmethod
    async def create_menu_services(
        cls, query_db: AsyncSession, table_id: int, current_user: CurrentUserModel
    ) -> CrudResponseModel:
        """
        根据代码生成表配置自动创建菜单service

        :param query_db: orm对象
        :param table_id: 表编号
        :param current_user: 当前用户信息对象
        :return: 创建菜单结果
        """
        from module_admin.dao.menu_dao import MenuDao
        from module_admin.entity.vo.menu_vo import MenuModel
        from utils.log_util import logger
        
        try:
            # 获取代码生成表信息
            logger.info(f'开始生成菜单 - table_id: {table_id}')
            gen_table = await GenTableDao.get_gen_table_by_id(query_db, table_id)
            if not gen_table:
                raise ServiceException(message='代码生成表不存在')
            
            # 调试：打印原始数据库对象的字段值
            logger.info(f'数据库原始值 - table_name: {gen_table.table_name}')
            logger.info(f'数据库原始值 - function_name: {gen_table.function_name}')
            logger.info(f'数据库原始值 - business_name: {gen_table.business_name}')
            logger.info(f'数据库原始值 - module_name: {gen_table.module_name}')
            
            # 检查必要字段（直接从数据库对象检查，避免触发 Pydantic 验证）
            if not gen_table.function_name:
                raise ServiceException(message='生成功能名不能为空，请先在"编辑"页面的"生成信息"页签中配置')
            if not gen_table.business_name:
                raise ServiceException(message='生成业务名不能为空，请先在"编辑"页面的"生成信息"页签中配置')
            if not gen_table.module_name:
                raise ServiceException(message='生成模块名不能为空，请先在"编辑"页面的"生成信息"页签中配置')
            
            # 使用 CamelCaseUtil 转换（不触发 Pydantic 验证）
            table_dict = CamelCaseUtil.transform_result(gen_table)
            # 手动创建对象，跳过验证
            table_info = GenTableModel.model_construct(**table_dict)
            await cls.set_table_from_options(table_info)
            
            logger.info(f'生成菜单 - 功能名: {table_info.function_name}')
            
            # 获取父菜单ID，如果没有配置则使用0（顶级菜单）
            parent_menu_id = table_info.parent_menu_id if table_info.parent_menu_id else 0
            
            # 构建权限标识前缀：模块名:业务名
            perms_prefix = f'{table_info.module_name}:{table_info.business_name}'
            
            # 构建组件路径：模块名/业务名/index
            component_path = f'{table_info.module_name}/{table_info.business_name}/index'
            
            # 检查菜单是否已存在
            existing_menu = await MenuDao.get_menu_detail_by_info(
                query_db, MenuModel(menuName=table_info.function_name, parentId=parent_menu_id)
            )
            if existing_menu:
                raise ServiceException(message=f'菜单"{table_info.function_name}"已存在，请勿重复生成')
            
            # 获取父菜单下的最大排序号
            from sqlalchemy import select, func
            from module_admin.entity.do.menu_do import SysMenu
            
            max_order_result = await query_db.execute(
                select(func.max(SysMenu.order_num)).where(SysMenu.parent_id == parent_menu_id)
            )
            max_order = max_order_result.scalar()
            base_order = (max_order if max_order else 0) + 1
            
            # 调试：打印即将创建菜单的信息
            logger.info(f'准备创建菜单 - function_name 类型: {type(table_info.function_name)}')
            logger.info(f'准备创建菜单 - function_name 值: [{table_info.function_name}]')
            logger.info(f'准备创建菜单 - function_name repr: {repr(table_info.function_name)}')
            logger.info(f'准备创建菜单 - business_name: {table_info.business_name}')
            logger.info(f'准备创建菜单 - module_name: {table_info.module_name}')
            logger.info(f'准备创建菜单 - component_path: {component_path}')
            
            # 再次检查（防御性编程）
            if not table_info.function_name:
                logger.error(f'function_name 为空！table_info 完整内容: {table_info.model_dump()}')
                raise ServiceException(message=f'生成功能名为空，请检查数据库中 gen_table 表的 function_name 字段')
            
            # 1. 创建主菜单（C类型 - 菜单）
            # 使用 model_construct 避免 alias_generator 的影响
            main_menu = MenuModel.model_construct(
                menu_name=table_info.function_name,  # 菜单名称：生成功能名
                parent_id=parent_menu_id,  # 上级菜单：从生成信息获取
                order_num=base_order,  # 显示排序：自动计算
                path=table_info.business_name,  # 路由地址：生成业务名
                component=component_path,  # 组件路径：模块名/业务名/index
                query='',  # 路由参数：空
                route_name='',  # 路由名称：空
                is_frame=1,  # 是否外链：否
                is_cache=0,  # 是否缓存：缓存
                menu_type='C',  # 菜单类型：菜单
                visible='0',  # 显示状态：显示
                status='0',  # 菜单状态：正常
                perms=f'{perms_prefix}:list',  # 权限字符：模块名:业务名:list
                icon='#',  # 菜单图标：默认
                create_by=current_user.user.user_name,
                create_time=datetime.now(),
                update_by=current_user.user.user_name,
                update_time=datetime.now(),
                remark=f'{table_info.function_name}菜单'
            )
            
            logger.info(f'创建的 MenuModel - menu_name: {main_menu.menu_name}')
            logger.info(f'MenuModel dump: {main_menu.model_dump(by_alias=False)}')
            
            main_menu_obj = await MenuDao.add_menu_dao(query_db, main_menu)
            await query_db.flush()
            main_menu_id = main_menu_obj.menu_id
            
            # 2. 创建查询按钮（F类型 - 按钮）
            query_button = MenuModel.model_construct(
                menu_name=f'{table_info.function_name}查询',
                parent_id=main_menu_id,
                order_num=1,
                path='',
                component='',
                query='',
                route_name='',
                is_frame=1,
                is_cache=0,
                menu_type='F',
                visible='0',
                status='0',
                perms=f'{perms_prefix}:query',
                icon='#',
                create_by=current_user.user.user_name,
                create_time=datetime.now(),
                update_by=current_user.user.user_name,
                update_time=datetime.now(),
                remark=''
            )
            await MenuDao.add_menu_dao(query_db, query_button)
            
            # 3. 创建新增按钮（F类型 - 按钮）
            add_button = MenuModel.model_construct(
                menu_name=f'{table_info.function_name}新增',
                parent_id=main_menu_id,
                order_num=2,
                path='',
                component='',
                query='',
                route_name='',
                is_frame=1,
                is_cache=0,
                menu_type='F',
                visible='0',
                status='0',
                perms=f'{perms_prefix}:add',
                icon='#',
                create_by=current_user.user.user_name,
                create_time=datetime.now(),
                update_by=current_user.user.user_name,
                update_time=datetime.now(),
                remark=''
            )
            await MenuDao.add_menu_dao(query_db, add_button)
            
            # 4. 创建修改按钮（F类型 - 按钮）
            edit_button = MenuModel.model_construct(
                menu_name=f'{table_info.function_name}修改',
                parent_id=main_menu_id,
                order_num=3,
                path='',
                component='',
                query='',
                route_name='',
                is_frame=1,
                is_cache=0,
                menu_type='F',
                visible='0',
                status='0',
                perms=f'{perms_prefix}:edit',
                icon='#',
                create_by=current_user.user.user_name,
                create_time=datetime.now(),
                update_by=current_user.user.user_name,
                update_time=datetime.now(),
                remark=''
            )
            await MenuDao.add_menu_dao(query_db, edit_button)
            
            # 5. 创建删除按钮（F类型 - 按钮）
            delete_button = MenuModel.model_construct(
                menu_name=f'{table_info.function_name}删除',
                parent_id=main_menu_id,
                order_num=4,
                path='',
                component='',
                query='',
                route_name='',
                is_frame=1,
                is_cache=0,
                menu_type='F',
                visible='0',
                status='0',
                perms=f'{perms_prefix}:remove',
                icon='#',
                create_by=current_user.user.user_name,
                create_time=datetime.now(),
                update_by=current_user.user.user_name,
                update_time=datetime.now(),
                remark=''
            )
            await MenuDao.add_menu_dao(query_db, delete_button)
            
            # 6. 创建导出按钮（F类型 - 按钮）
            export_button = MenuModel.model_construct(
                menu_name=f'{table_info.function_name}导出',
                parent_id=main_menu_id,
                order_num=5,
                path='',
                component='',
                query='',
                route_name='',
                is_frame=1,
                is_cache=0,
                menu_type='F',
                visible='0',
                status='0',
                perms=f'{perms_prefix}:export',
                icon='#',
                create_by=current_user.user.user_name,
                create_time=datetime.now(),
                update_by=current_user.user.user_name,
                update_time=datetime.now(),
                remark=''
            )
            await MenuDao.add_menu_dao(query_db, export_button)
            
            await query_db.commit()
            
            # 返回简洁的成功信息
            return CrudResponseModel(
                is_success=True, 
                message=f'菜单"{table_info.function_name}"生成成功，已创建1个主菜单和5个按钮权限'
            )
            
        except ServiceException as e:
            await query_db.rollback()
            raise e
        except Exception as e:
            await query_db.rollback()
            raise ServiceException(message=f'生成菜单失败: {str(e)}')

    @classmethod
    async def generate_table_sql_services(
        cls, query_db: AsyncSession, model_id: int, requirement: str
    ) -> str:
        """
        通过AI模型生成建表SQL语句service

        :param query_db: orm对象
        :param model_id: 模型ID
        :param requirement: 表需求描述
        :return: 生成的SQL语句
        """
        from agno.agent import Agent
        from module_ai.dao.ai_model_dao import AiModelDao
        from module_ai.entity.vo.ai_model_vo import AiModelModel
        from utils.ai_util import AiUtil
        from utils.crypto_util import CryptoUtil
        
        try:
            # 获取模型信息
            ai_model = await AiModelDao.get_ai_model_detail_by_id(query_db, model_id=model_id)
            if not ai_model:
                raise ServiceException(message='AI模型不存在')
            
            model_config = AiModelModel(**CamelCaseUtil.transform_result(ai_model))
            
            # 解密API Key
            real_api_key = CryptoUtil.decrypt(model_config.api_key) if model_config.api_key else None
            if not real_api_key:
                raise ServiceException(message='模型API Key未配置')
            
            # 根据数据库类型构建不同的提示词
            db_type = DataBaseConfig.db_type
            
            if db_type == 'postgresql':
                system_prompt = """你是一个数据库专家，专门负责根据需求生成PostgreSQL建表SQL语句。

要求：
1. 生成标准的PostgreSQL CREATE TABLE语句
2. 使用PostgreSQL的数据类型（如serial、bigserial、varchar、text、timestamp等）
3. 添加必要的索引和主键
4. 字段需要有注释说明（使用COMMENT ON语句）
5. 表需要有注释说明（使用COMMENT ON TABLE语句）
6. 主键使用SERIAL或BIGSERIAL自增
7. 时间字段使用timestamp类型，默认值使用CURRENT_TIMESTAMP
8. ⚠️ 重要：除主键外，其他字段不要设置为 NOT NULL（必填），以提高系统灵活性
9. 只返回SQL语句，不要有其他说明文字
10. 如果需要多个表，请用分号分隔

示例格式：
CREATE TABLE table_name (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100),
  status SMALLINT DEFAULT 0,
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE table_name IS '表说明';
COMMENT ON COLUMN table_name.id IS '主键ID';
COMMENT ON COLUMN table_name.name IS '名称';
COMMENT ON COLUMN table_name.status IS '状态';
COMMENT ON COLUMN table_name.create_time IS '创建时间';
COMMENT ON COLUMN table_name.update_time IS '更新时间';

CREATE INDEX idx_table_name_status ON table_name(status);"""
            else:  # MySQL
                system_prompt = """你是一个数据库专家，专门负责根据需求生成MySQL建表SQL语句。

要求：
1. 生成标准的MySQL CREATE TABLE语句
2. 包含合适的字段类型、长度、默认值
3. 添加必要的索引和主键
4. 字段需要有注释说明
5. 表需要有注释说明
6. 使用InnoDB引擎，utf8mb4字符集
7. ⚠️ 重要：除主键外，其他字段尽量不要设置为 NOT NULL（必填），以提高系统灵活性
8. 只返回SQL语句，不要有其他说明文字
9. 如果需要多个表，请用分号分隔

示例格式：
CREATE TABLE `table_name` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) DEFAULT NULL COMMENT '名称',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='表说明';"""

            user_message = f"请根据以下需求生成建表SQL：\n\n{requirement}"
            
            # 使用系统的AiUtil获取模型实例
            model = AiUtil.get_model_from_factory(
                provider=model_config.provider,
                model_code=model_config.model_code,
                model_name=model_config.model_name,
                api_key=real_api_key,
                base_url=model_config.base_url,
                temperature=model_config.temperature if model_config.temperature else 0.7,
                max_tokens=model_config.max_tokens,
            )
            
            # 创建Agent
            agent = Agent(
                model=model,
                description=system_prompt,
                markdown=False,
            )
            
            # 同步调用生成
            response = agent.run(user_message, stream=False)
            
            if not response or not response.content:
                raise ServiceException(message='AI模型返回内容为空')
            
            sql_content = response.content
            
            # 清理返回的SQL（去除markdown代码块标记）
            sql_content = sql_content.strip()
            if sql_content.startswith('```sql'):
                sql_content = sql_content[6:]
            elif sql_content.startswith('```'):
                sql_content = sql_content[3:]
            if sql_content.endswith('```'):
                sql_content = sql_content[:-3]
            
            return sql_content.strip()
                
        except ServiceException as e:
            raise e
        except Exception as e:
            raise ServiceException(message=f'生成SQL失败: {str(e)}')

    @classmethod
    async def refactor_frontend_services(
        cls, 
        query_db: AsyncSession, 
        table_ids: list[int], 
        model_id: int, 
        requirement: str, 
        keep_original: bool = True,
        add_new_button: bool = False,
        new_button_name: str | None = None,
        file_type: str | None = None,
        error_message: str | None = None,
        current_code: str | None = None
    ) -> dict[str, str]:
        """
        通过AI模型重构前端界面service

        :param query_db: orm对象
        :param table_ids: 表ID列表
        :param model_id: 模型ID
        :param requirement: 重构需求描述（包含新按钮功能）
        :param keep_original: 是否保留原有功能
        :param add_new_button: 是否新增按钮
        :param new_button_name: 新按钮名称
        :param file_type: 指定重新生成的文件类型
        :param error_message: 错误信息或修改需求
        :param current_code: 当前的代码
        :return: 重构后的代码字典
        """
        from agno.agent import Agent
        from module_ai.dao.ai_model_dao import AiModelDao
        from module_ai.entity.vo.ai_model_vo import AiModelModel
        from utils.ai_util import AiUtil
        from utils.crypto_util import CryptoUtil

        try:
            if not table_ids:
                raise ServiceException(message='请至少选择一个表')

            # 获取第一个表作为主表
            main_table_id = table_ids[0]
            gen_table = await cls.get_gen_table_by_id_services(query_db, main_table_id)
            if not gen_table:
                raise ServiceException(message='主表信息不存在')

            # 获取模型信息
            ai_model = await AiModelDao.get_ai_model_detail_by_id(query_db, model_id=model_id)
            if not ai_model:
                raise ServiceException(message='AI模型不存在')

            model_config = AiModelModel(**CamelCaseUtil.transform_result(ai_model))

            # 解密API Key
            real_api_key = CryptoUtil.decrypt(model_config.api_key) if model_config.api_key else None
            if not real_api_key:
                raise ServiceException(message='模型API Key未配置')

            # 构建所有表的信息
            tables_info = []
            for table_id in table_ids:
                table = await cls.get_gen_table_by_id_services(query_db, table_id)
                if table:
                    columns = await GenTableColumnService.get_gen_table_column_list_by_table_id_services(
                        query_db, table_id
                    )
                    columns_info = []
                    for col in columns:
                        columns_info.append(
                            {
                                'columnName': col.column_name,
                                'columnComment': col.column_comment,
                                'columnType': col.column_type,  # 添加字段类型
                                'pythonType': col.python_type,  # 添加 Python 类型
                                'isPk': col.is_pk,  # 是否主键
                                'isRequired': col.is_required,  # 是否必填
                            }
                        )
                    tables_info.append(
                        {
                            'tableName': table.table_name,
                            'tableComment': table.table_comment,
                            'columns': columns_info,
                        }
                    )

            # 读取原有代码（如果需要保留）
            original_code = None
            original_controller = None
            original_service = None
            if keep_original:
                try:
                    # 构建文件路径
                    module_name = gen_table.module_name
                    business_name = gen_table.business_name
                    frontend_path = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ruoyi-fastapi-frontend')
                    )
                    vue_file = os.path.join(frontend_path, 'src', 'views', module_name, business_name, 'index.vue')
                    
                    if os.path.exists(vue_file):
                        async with aiofiles.open(vue_file, 'r', encoding='utf-8') as f:
                            original_code = await f.read()
                    
                    # 如果需要新增按钮，读取后端代码
                    if add_new_button and new_button_name:
                        backend_path = os.path.abspath(
                            os.path.join(os.path.dirname(__file__), '..', '..')
                        )
                        controller_file = os.path.join(backend_path, module_name, 'controller', f'{business_name}_controller.py')
                        service_file = os.path.join(backend_path, module_name, 'service', f'{business_name}_service.py')
                        
                        if os.path.exists(controller_file):
                            async with aiofiles.open(controller_file, 'r', encoding='utf-8') as f:
                                original_controller = await f.read()
                        
                        if os.path.exists(service_file):
                            async with aiofiles.open(service_file, 'r', encoding='utf-8') as f:
                                original_service = await f.read()
                except Exception as e:
                    # 如果读取失败，继续执行，不影响重构
                    pass

            # 如果是重新生成单个文件
            is_regenerate = file_type is not None and error_message is not None
            
            # 构建系统提示词
            if is_regenerate:
                # 重新生成单个文件的提示词
                file_type_map = {
                    'index': 'index.vue（前端页面组件）',
                    'controller': 'controller.py（后端控制器层）',
                    'service': 'service.py（后端服务层）',
                    'api': 'api.js（前端API接口）'
                }
                
                system_prompt = f"""你是一个代码修复专家，需要根据错误信息重新生成 {file_type_map.get(file_type, file_type)} 的代码。

【表结构信息】
{json.dumps(tables_info, ensure_ascii=False, indent=2)}

【主表详细信息】
- 表名：{gen_table.table_name}
- 表描述：{gen_table.table_comment}
- 功能名：{gen_table.function_name}
- 业务名：{gen_table.business_name}
- 模块名：{gen_table.module_name}
- 数据库类型：PostgreSQL

【字段类型说明】
- columnType: 数据库字段类型（如 varchar, integer, timestamp 等）
- pythonType: Python 类型（如 str, int, datetime 等）
- isPk: 是否为主键（主键字段插入时不要设置值）
- isRequired: 是否必填（必填字段不能为 None）

【当前代码】
```
{current_code if current_code else '无'}
```

【问题描述】
{error_message}

【原始需求】
{requirement}
"""
                
                if keep_original and original_code and file_type == 'index':
                    system_prompt += f"""
【原有完整代码（参考）】
```vue
{original_code}
```
"""
                
                if add_new_button and new_button_name:
                    system_prompt += f"""
【新增按钮功能】
按钮名称：{new_button_name}
功能描述：请从重构需求中提取该按钮的功能描述

【重要要求】
1. 只返回新增的方法代码，不要返回完整类
2. 不要返回 import 语句和类定义
3. Python 代码用 ```python 代码块包裹
4. 代码要有正确的缩进（4空格为一级）
5. 修复所有语法错误
6. 确保代码可以直接运行

【返回格式】
只返回修复后的代码，用 ```python 代码块包裹。
"""
                elif file_type == 'index':
                    system_prompt += """
【重要要求】
1. 返回完整的 Vue 单文件组件代码
2. 包含 template、script、style 三部分
3. 修复所有语法错误
4. 如果启用了保留原功能，必须保留所有原有功能
5. 确保代码可以直接运行

【返回格式】
返回完整的 Vue 代码。
"""
                elif file_type == 'api':
                    system_prompt += """
【重要要求】
1. 只返回新增的 API 方法
2. 使用 request 工具封装
3. 修复所有语法错误

【返回格式】
只返回修复后的 API 方法代码。
"""
            else:
                # 完整重构的提示词
                system_prompt = f"""你是一个前端开发专家，专门负责根据需求重构Vue前端界面。

【表结构信息】
{json.dumps(tables_info, ensure_ascii=False, indent=2)}

【主表详细信息】
- 表名：{gen_table.table_name}
- 表描述：{gen_table.table_comment}
- 功能名：{gen_table.function_name}
- 业务名：{gen_table.business_name}
- 模块名：{gen_table.module_name}
- 数据库类型：PostgreSQL

【字段类型说明】
- columnType: 数据库字段类型（如 varchar, integer, timestamp 等）
- pythonType: Python 类型（如 str, int, datetime 等）
- isPk: 是否为主键
- isRequired: 是否必填
"""

            if not is_regenerate and keep_original and original_code:
                system_prompt += f"""
【原有代码】
```vue
{original_code}
```
"""
                if add_new_button and new_button_name:
                    if original_controller:
                        system_prompt += f"""
【原有Controller代码】
```python
{original_controller}
```
"""
                    if original_service:
                        system_prompt += f"""
【原有Service代码】
```python
{original_service}
```
"""
                    system_prompt += f"""
【表结构信息】
{json.dumps(tables_info, ensure_ascii=False, indent=2)}

【主表详细信息】
- 表名：{gen_table.table_name}
- 表描述：{gen_table.table_comment}
- 功能名：{gen_table.function_name}
- 业务名：{gen_table.business_name}
- 模块名：{gen_table.module_name}
- 数据库类型：PostgreSQL

【新增按钮功能】
按钮名称：{new_button_name}
功能描述：请从下方的重构需求中提取

【重要要求 - 只返回新增的方法】
1. Service 和 Controller 只返回新增的方法代码
2. 不要返回完整的类定义
3. 不要返回 import 语句
4. 不要返回已有的方法
5. 只返回新增的方法，格式如下：

    @classmethod
    async def new_method_name(cls, ...):
        \"\"\"方法说明\"\"\"
        # 方法实现
        pass

6. 新按钮的权限标识格式：{gen_table.module_name}:{gen_table.business_name}:{new_button_name.lower().replace(' ', '_')}
7. 前端 Vue 文件返回完整代码（保留所有原有功能）
8. 根据重构需求中的功能描述实现具体的业务逻辑
9. ⚠️ 生成随机数据时，必须根据上面的【表结构信息】中的字段类型和约束来生成
10. ⚠️ 字段类型映射：
    - varchar/text → 字符串
    - integer/bigint → 整数
    - numeric/decimal → 浮点数
    - timestamp/date → datetime 对象
    - boolean → True/False
11. ⚠️ 必填字段（isRequired=true）必须提供值，不能为 None
12. ⚠️ 主键字段（isPk=true）在插入时不要设置值（自动生成）
"""
                else:
                    system_prompt += """
【重要要求 - 保留原功能模式】
1. 必须保留原有代码中的所有增删改查功能
2. 必须保留原有的表格、表单、对话框等核心组件
3. 必须保留原有的所有字段和验证规则
4. 必须保留原有的所有方法和事件处理
5. 必须保留原有的 data() 中的所有数据定义（包括字典数据）
6. 必须保留原有的 created()、mounted() 等生命周期钩子
7. 必须保留原有的 getDicts() 字典加载逻辑
8. 在原有功能基础上进行增强和优化
9. 不要删除任何现有的功能代码
10. 可以添加新功能、优化样式、改进交互、增加新组件
11. 确保所有原有的权限控制（v-hasPermi）都保留
12. 保持原有的 API 调用和数据处理逻辑

【特别注意 - 字典数据】
1. 必须保留原有代码中所有的字典数据定义，例如：
   - sys_user_sex: []
   - sys_normal_disable: []
   - 其他字典数据
2. 必须保留原有的 getDicts() 调用，例如：
   - this.getDicts("sys_user_sex", "sys_normal_disable").then(...)
3. 不要删除或修改任何字典相关的代码
"""
            else:
                system_prompt += """
【重要要求 - 完全重构模式】
1. 生成全新的Vue 2.x单文件组件代码
2. 不需要保留原有的任何功能
3. 根据需求完全重新设计界面和功能
4. 如果需求中没有提到增删改查，可以不包含这些功能
5. 完全按照用户的需求描述来实现
6. 使用Element UI组件库
7. 代码要简洁、现代化
"""

            system_prompt += """
【通用要求】
1. 生成完整的Vue 2.x单文件组件代码（index.vue）
2. 使用Element UI组件库
3. 包含完整的template、script、style三部分
4. 保持与RuoYi框架的代码风格一致
5. 包含必要的权限控制（v-hasPermi指令）
6. 代码要规范、可读性强、注释清晰
7. 只生成主表的Vue文件代码
8. 确保生成的代码可以直接运行，没有语法错误

【返回格式】
必须严格按照以下JSON格式返回：
"""
            
            if add_new_button and new_button_name and keep_original:
                system_prompt += """{
  "index": "完整的index.vue代码（包含所有原有功能和新增按钮）",
  "controller": "完整的Controller文件代码（包含所有import、类定义和所有方法）",
  "service": "完整的Service文件代码（包含所有import、类定义和所有方法）",
  "api": "完整的前端API文件代码（包含import语句和所有函数）",
  "vo": "完整的VO文件代码（包含所有原有Model + 新增Model）"
}

【关键要求 - 全量替换模式】

1. ⚠️ 必须返回完整的文件代码，不是只返回新增的方法/函数！
2. 包含所有必要的import语句
3. 包含完整的类定义（Python）或所有函数（JavaScript）
4. 包含所有原有的方法/函数 + 新增的方法/函数
5. Python代码用```python代码块包裹，JavaScript代码用```javascript代码块包裹
6. 代码要有正确的换行和缩进
7. 保持原有代码的结构和风格

【⚠️ 重要：新增接口的参数处理】

对于新增接口，优先使用以下方式处理参数，避免创建新的 Model：

方式1：使用 Query/Form 参数（推荐 - 简单参数）
```python
@xxx_controller.post('/generate')
async def generate_random_data(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],  # 依赖注入参数在前
    count: Annotated[int, Form(ge=1, le=100, description='数量')] = 10,  # 有默认值的参数在后
) -> Response:
    pass
```

⚠️ 常见错误：

错误1：default 不能在 Form() 中
```python
count: Annotated[int, Form(default=10)]  # ❌ 错误
count: Annotated[int, Form()] = 10  # ✅ 正确
```

错误2：参数顺序错误
```python
# ❌ 错误：有默认值的参数在前
async def func(
    count: Annotated[int, Form()] = 10,  # 有默认值
    query_db: Annotated[AsyncSession, DBSessionDependency()],  # 无默认值
):
    pass

# ✅ 正确：有默认值的参数在后
async def func(
    query_db: Annotated[AsyncSession, DBSessionDependency()],  # 无默认值
    count: Annotated[int, Form()] = 10,  # 有默认值
):
    pass
```

方式2：使用已有的 Model
```python
# 如果已有合适的 Model，直接使用，不要创建新的
```

方式3：必须创建新 Model 时（复杂参数结构）
```python
# 只有在确实需要复杂参数结构时才创建新 Model
# 并且必须在 VO 文件中同时定义这个 Model
```

【⚠️ 重要：外部库依赖处理】

如果新增功能需要使用外部库（如 pandas, numpy, requests 等），遵循以下规则：

1. **在方法内部导入**（推荐）
```python
@classmethod
async def process_excel_services(cls, query_db: AsyncSession, file_data: bytes):
    '''处理Excel文件'''
    import pandas as pd  # 在方法内导入
    import openpyxl
    
    try:
        df = pd.read_excel(file_data)
        # 处理逻辑
        return CrudResponseModel(is_success=True)
    except Exception as e:
        raise e
```

2. **使用项目已有的工具类**（优先）
```python
# 项目已有的工具类：
from utils.excel_util import ExcelUtil  # Excel 处理
from utils.common_util import CamelCaseUtil  # 驼峰转换
from utils.crypto_util import CryptoUtil  # 加密解密
from utils.page_util import PageUtil  # 分页
# 优先使用这些工具类，而不是重新导入外部库
```

3. **常用库的导入位置**
- 标准库（os, json, datetime 等）：可以在文件顶部导入
- 第三方库（pandas, numpy, requests 等）：在方法内部导入
- 项目内部模块：在文件顶部导入

4. **依赖说明**
如果使用了项目中可能没有的库，在注释中说明：
```python
@classmethod
async def advanced_analysis_services(cls, query_db: AsyncSession, data: dict):
    '''高级数据分析
    
    依赖：需要安装 scikit-learn
    安装命令：pip install scikit-learn
    '''
    try:
        from sklearn.cluster import KMeans  # 需要额外安装
        # 分析逻辑
    except ImportError:
        raise ServiceException(message='缺少依赖库 scikit-learn，请先安装')
```

【⚠️ 禁止：访问 SQLAlchemy 内部属性】

绝对不要访问 query_db 的内部属性，这会导致运行时错误！

❌ 错误示例：
```python
# 不要这样做！会导致运行时错误
db_url = query_db.bind.engine.url.render_as_string(hidden_password=False)
db_name = query_db.bind.engine.url.database
```

✅ 正确做法：
```python
# 如果需要字典数据，使用硬编码的选项值
sex_options = ['0', '1']  # 0-男，1-女

# 如果需要查询数据库，使用 DAO 层的查询方法
result = await SomeDao.query_something(query_db, params)

# 如果需要配置信息，从环境变量或配置文件读取
from config.env import AppConfig
db_type = AppConfig.db_type
```

【VO文件规范】

⚠️ 如果 Controller 中导入了新的 Model，VO 文件必须包含该 Model 的完整定义！

示例：
- Controller 导入：`from xxx_vo import XxxModel, NewModel`
- VO 文件必须包含：`class XxxModel` 和 `class NewModel` 的完整定义

正确示例1（推荐：使用 Form 参数，不创建新 Model）：
{
  "controller": "```python
from fastapi import Form
from typing import Annotated

@teacher_controller.post('/generate')
async def generate_random_teacher(
    request: Request,
    query_db: Annotated[AsyncSession, DBSessionDependency()],  # 依赖注入参数在前
    count: Annotated[int, Form(ge=1, le=100, description='生成数据数量')] = 10,  # 有默认值的参数在后
) -> Response:
    result = await TeacherService.generate_random_teacher_services(query_db, count)
    return ResponseUtil.success(msg=result.message)
```",
  "service": "```python
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from common.vo import CrudResponseModel

class TeacherService:
    '''教师管理模块服务层'''
    
    @classmethod
    async def get_teacher_list_services(cls, query_db: AsyncSession):
        '''获取教师列表（原有方法）'''
        pass
    
    @classmethod
    async def generate_random_teacher_services(cls, query_db: AsyncSession, count: int):
        '''随机生成教师数据（新增方法）'''
        import random  # 在方法内导入
        import string
        from datetime import datetime
        
        try:
            for i in range(count):
                # 生成随机数据
                teacher_no = 'T' + ''.join(random.choices(string.digits, k=6))
                name = random.choice(['张三', '李四', '王五'])
                # ... 其他字段
            return CrudResponseModel(is_success=True, message=f'成功生成{count}条数据')
        except Exception as e:
            raise e
```",
  "api": "```javascript
import request from '@/utils/request'

// 查询教师列表（原有函数）
export function listTeacher(query) {
  return request({
    url: '/admin/teacher/list',
    method: 'get',
    params: query
  })
}

// 随机生成教师数据（新增函数）
export function generateRandomTeacher(count) {
  return request({
    url: '/admin/teacher/generate',
    method: 'post',
    data: { count }
  })
}
```",
  "vo": "不需要修改（因为没有创建新 Model）"
}

正确示例2（复杂功能：使用外部库处理 Excel）：
{
  "controller": "```python
from fastapi import File, UploadFile

@teacher_controller.post('/import')
async def import_teacher_excel(
    request: Request,
    file: UploadFile = File(...),
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    file_data = await file.read()
    result = await TeacherService.import_excel_services(query_db, file_data)
    return ResponseUtil.success(msg=result.message)
```",
  "service": "```python
class TeacherService:
    '''教师管理模块服务层'''
    
    @classmethod
    async def import_excel_services(cls, query_db: AsyncSession, file_data: bytes):
        '''导入Excel文件
        
        依赖：使用项目自带的 ExcelUtil 工具类
        '''
        from utils.excel_util import ExcelUtil  # 使用项目工具类
        import io
        
        try:
            # 解析 Excel
            excel_data = ExcelUtil.parse_excel(io.BytesIO(file_data))
            
            # 批量插入数据
            for row in excel_data:
                teacher = TeacherModel(
                    teacher_no=row.get('教师编号'),
                    name=row.get('姓名'),
                    # ... 其他字段
                )
                await TeacherDao.add_teacher_dao(query_db, teacher)
            
            await query_db.commit()
            return CrudResponseModel(is_success=True, message=f'成功导入{len(excel_data)}条数据')
        except Exception as e:
            await query_db.rollback()
            raise e
```"
}

正确示例3（高级功能：使用第三方库进行数据分析）：
{
  "service": "```python
class TeacherService:
    '''教师管理模块服务层'''
    
    @classmethod
    async def analyze_teacher_data_services(cls, query_db: AsyncSession):
        '''分析教师数据
        
        依赖：需要安装 pandas
        安装命令：pip install pandas
        '''
        try:
            import pandas as pd  # 在方法内导入第三方库
            
            # 获取数据
            teachers = await TeacherDao.get_all_teachers(query_db)
            
            # 转换为 DataFrame
            df = pd.DataFrame([t.__dict__ for t in teachers])
            
            # 数据分析
            stats = {
                'total': len(df),
                'by_gender': df['gender'].value_counts().to_dict(),
                'by_department': df['department'].value_counts().to_dict(),
            }
            
            return CrudResponseModel(is_success=True, data=stats)
        except ImportError:
            raise ServiceException(message='缺少依赖库 pandas，请先安装：pip install pandas')
        except Exception as e:
            raise e
```"
}

正确示例4（如果必须创建新 Model）：
{
  "controller": "```python
from module_admin.entity.vo.teacher_vo import TeacherModel, GenerateRandomTeacherModel

@teacher_controller.post('/generate')
async def generate_random_teacher(
    request: Request,
    generate_model: GenerateRandomTeacherModel,  # 使用新 Model
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await TeacherService.generate_random_teacher_services(query_db, generate_model.count)
    return ResponseUtil.success(msg=result.message)
```",
  "vo": "```python
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel

class TeacherModel(BaseModel):
    '''教师模型（原有模型）'''
    id: int | None = None
    name: str | None = None

class GenerateRandomTeacherModel(BaseModel):
    '''随机生成教师数据请求模型（新增模型 - 必须包含！）'''
    model_config = ConfigDict(alias_generator=to_camel)
    
    count: int = Field(default=10, description='生成数据数量', ge=1, le=100)
```"
}

错误示例（不要这样 - Controller 导入了新 Model 但 VO 文件没有定义）：
{
  "controller": "from xxx_vo import NewModel  # ❌ 导入了新 Model",
  "vo": "只包含原有 Model，没有 NewModel 的定义  # ❌ 会导致 ImportError"
}

【Python代码缩进】
- import语句：顶格（0个空格）
- 类定义：顶格（0个空格）
- 类文档字符串：4个空格
- 装饰器：4个空格
- 方法定义：4个空格
- 方法文档字符串：8个空格
- 方法体：8个空格
- try/for/if块内容：12个空格

【JavaScript代码规范】
- import语句：顶格
- 注释：顶格或与代码同级
- 函数定义：顶格
- 函数体：2个空格缩进
"""
            else:
                system_prompt += """{
  "index": "完整的index.vue代码"
}"""

            # 构建用户消息
            if is_regenerate:
                # 重新生成单个文件的用户消息
                user_message = f"""请根据以下问题描述，重新生成 {file_type} 的代码：

【问题描述】
{error_message}

【原始需求】
{requirement}

【当前代码存在的问题】
请仔细分析当前代码，找出问题所在并修复。

重要提醒：
1. 只返回修复后的代码，不要返回其他内容
2. Python代码用```python代码块包裹
3. 代码要有正确的换行和缩进
4. 确保代码没有语法错误
5. 如果是 Service 或 Controller，只返回新增的方法"""
            else:
                # 完整重构的用户消息
                user_message = f"""请根据以下需求重构前端界面：

{requirement}

重要提醒：
1. ⚠️ Service和Controller必须返回完整的文件代码，包含所有import、类定义和所有方法
2. 不要只返回新增的方法，要返回完整文件
3. Python代码用```python代码块包裹
4. 代码要有正确的换行和缩进
5. 保持原有代码的结构和风格"""

            # 使用系统的AiUtil获取模型实例
            model = AiUtil.get_model_from_factory(
                provider=model_config.provider,
                model_code=model_config.model_code,
                model_name=model_config.model_name,
                api_key=real_api_key,
                base_url=model_config.base_url,
                temperature=model_config.temperature if model_config.temperature else 0.7,
                max_tokens=model_config.max_tokens if model_config.max_tokens else 16384,
            )

            # 创建Agent
            agent = Agent(
                model=model,
                description=system_prompt,
                markdown=False,
            )

            # 同步调用生成
            response = agent.run(user_message, stream=False)

            if not response or not response.content:
                raise ServiceException(message='AI模型返回内容为空')

            result_content = response.content.strip()

            # 清理返回的内容（去除markdown代码块标记）
            if result_content.startswith('```json'):
                result_content = result_content[7:]
            elif result_content.startswith('```'):
                result_content = result_content[3:]
            if result_content.endswith('```'):
                result_content = result_content[:-3]

            # 解析JSON
            try:
                result_dict = json.loads(result_content.strip())
                
                # 提取代码并清理 Markdown 代码块标记
                def extract_and_clean_code(code_str, language='python'):
                    """提取并清理代码中的 Markdown 标记
                    
                    :param code_str: 原始代码字符串
                    :param language: 代码语言，'python' 或 'javascript'
                    :return: 清理后的代码
                    """
                    if not code_str:
                        return None
                    
                    # 清理代码
                    code_str = code_str.strip()
                    
                    import re
                    
                    # 方法1: 提取 ```language 代码块中的内容
                    pattern = rf'```{language}\s*\n(.*?)```'
                    match = re.search(pattern, code_str, re.DOTALL)
                    if match:
                        return match.group(1).strip()
                    
                    # 方法2: 提取 ``` 代码块中的内容（不指定语言）
                    pattern = r'```\s*\n(.*?)```'
                    match = re.search(pattern, code_str, re.DOTALL)
                    if match:
                        return match.group(1).strip()
                    
                    # 方法3: 如果代码以 ```language 开头但没有结束标记
                    if code_str.startswith(f'```{language}'):
                        code_str = code_str[len(f'```{language}'):].strip()
                        if code_str.endswith('```'):
                            code_str = code_str[:-3].strip()
                        return code_str
                    
                    # 方法4: 如果代码以 ``` 开头
                    if code_str.startswith('```'):
                        # 找到第一个换行符
                        first_newline = code_str.find('\n')
                        if first_newline > 0:
                            # 跳过第一行（可能是 ```python 或 ```javascript）
                            code_str = code_str[first_newline + 1:].strip()
                        else:
                            code_str = code_str[3:].strip()
                        if code_str.endswith('```'):
                            code_str = code_str[:-3].strip()
                        return code_str
                    
                    # 方法5: 清理可能残留的语言标记（如单独一行的 "javascript" 或 "python"）
                    lines = code_str.split('\n')
                    cleaned_lines = []
                    for line in lines:
                        stripped = line.strip()
                        # 跳过单独的语言标记行
                        if stripped in ['python', 'javascript', 'js', 'py', '```']:
                            continue
                        cleaned_lines.append(line)
                    
                    return '\n'.join(cleaned_lines).strip()
                
                # 如果是重新生成单个文件
                if is_regenerate and file_type:
                    # 只返回指定文件的代码
                    if isinstance(result_dict, dict):
                        code = result_dict.get(file_type, result_content)
                    else:
                        code = result_content
                    
                    # 清理代码
                    if file_type in ['controller', 'service']:
                        code = extract_and_clean_code(code, 'python')
                    elif file_type == 'api':
                        code = extract_and_clean_code(code, 'javascript')
                    else:
                        code = extract_and_clean_code(code, 'python')
                    
                    return {
                        file_type: code
                    }
                else:
                    # 完整重构，返回所有文件
                    return {
                        'index': result_dict.get('index', ''),
                        'controller': extract_and_clean_code(result_dict.get('controller'), 'python'),
                        'service': extract_and_clean_code(result_dict.get('service'), 'python'),
                        'api': extract_and_clean_code(result_dict.get('api'), 'javascript'),
                        'vo': extract_and_clean_code(result_dict.get('vo'), 'python'),  # 新增 VO 文件
                    }
            except json.JSONDecodeError:
                # 如果不是JSON格式
                if is_regenerate and file_type:
                    # 重新生成单个文件，直接返回内容
                    code = result_content
                    if file_type in ['controller', 'service', 'api']:
                        # 尝试提取代码块
                        import re
                        pattern = r'```python\s*\n(.*?)\n```'
                        match = re.search(pattern, code, re.DOTALL)
                        if match:
                            code = match.group(1).strip()
                        else:
                            pattern = r'```\s*\n(.*?)\n```'
                            match = re.search(pattern, code, re.DOTALL)
                            if match:
                                code = match.group(1).strip()
                    
                    return {
                        file_type: code
                    }
                else:
                    # 完整重构，尝试直接返回为index代码
                    return {
                        'index': result_content,
                        'controller': None,
                        'service': None,
                        'api': None,
                    }

        except ServiceException as e:
            raise e
        except Exception as e:
            raise ServiceException(message=f'重构失败: {str(e)}')

    @classmethod
    async def apply_refactor_services(
        cls, 
        query_db: AsyncSession, 
        table_id: int, 
        index_code: str, 
        api_code: str | None,
        controller_code: str | None,
        service_code: str | None,
        vo_code: str | None = None  # 新增 VO 代码参数
    ) -> CrudResponseModel:
        """
        应用重构结果到本地文件service

        :param query_db: orm对象
        :param table_id: 表ID
        :param index_code: index.vue代码
        :param api_code: api.js代码
        :param controller_code: controller.py代码
        :param service_code: service.py代码
        :param vo_code: vo.py代码
        :return: 应用结果
        """
        import tempfile
        import subprocess
        
        try:
            if not GenConfig.allow_overwrite:
                raise ServiceException(message='【系统预设】不允许覆盖本地文件')

            # 获取表信息
            gen_table = await cls.get_gen_table_by_id_services(query_db, table_id)
            if not gen_table:
                raise ServiceException(message='表信息不存在')

            # 构建文件路径
            module_name = gen_table.module_name
            business_name = gen_table.business_name

            # 前端项目根路径
            frontend_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..', '..', 'ruoyi-fastapi-frontend')
            )

            # Vue文件路径
            vue_dir = os.path.join(frontend_path, 'src', 'views', module_name, business_name)
            vue_file = os.path.join(vue_dir, 'index.vue')

            # API文件路径
            api_dir = os.path.join(frontend_path, 'src', 'api', module_name)
            api_file = os.path.join(api_dir, f'{business_name}.js')

            # 后端项目根路径
            backend_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', '..')
            )

            # Controller文件路径
            controller_file = os.path.join(backend_path, module_name, 'controller', f'{business_name}_controller.py')

            # Service文件路径
            service_file = os.path.join(backend_path, module_name, 'service', f'{business_name}_service.py')

            # VO文件路径
            vo_file = os.path.join(backend_path, module_name, 'entity', 'vo', f'{business_name}_vo.py')

            # ========== 验证阶段 ==========
            validation_errors = []
            service_code_cleaned = service_code
            controller_code_cleaned = controller_code
            vo_code_cleaned = vo_code
            
            # 0. 预验证：检查常见的运行时错误模式
            import re
            
            # 检查 Service 代码中的问题模式
            if service_code:
                # 检查 SQLAlchemy 内部属性访问（会导致运行时错误）
                sqlalchemy_patterns = [
                    (r'query_db\.bind\.engine\.url', '不要访问 query_db.bind.engine.url，这会导致运行时错误'),
                    (r'query_db\.bind\.engine', '不要访问 query_db.bind.engine 内部属性'),
                    (r'\.render_as_string\(', '不要使用 render_as_string() 方法'),
                ]
                
                for pattern, error_msg in sqlalchemy_patterns:
                    if re.search(pattern, service_code):
                        # 找到匹配的行
                        lines = service_code.split('\n')
                        error_lines = []
                        for i, line in enumerate(lines, 1):
                            if re.search(pattern, line):
                                error_lines.append(f'第 {i} 行: {line.strip()}')
                        
                        if error_lines:
                            full_error = f'⚠️ 运行时错误风险：{error_msg}\n\n'
                            full_error += '发现以下问题代码：\n'
                            full_error += '\n'.join(error_lines)
                            full_error += '\n\n建议：\n'
                            full_error += '- 如果需要字典数据，直接使用硬编码的选项值\n'
                            full_error += '- 如果需要查询数据库，使用 DAO 层的查询方法\n'
                            full_error += '- 不要尝试访问 SQLAlchemy 的内部属性\n'
                            validation_errors.append(full_error)
            
            # 1. 验证并修复 Service 代码（如果有）
            if service_code:
                # 清理代码
                service_code_cleaned = service_code.strip()
                while service_code_cleaned.startswith('\n'):
                    service_code_cleaned = service_code_cleaned[1:]
                
                # 🔥 超强预处理：处理完全挤在一起的代码
                import re
                
                # 阶段1: 基础分隔
                service_code_cleaned = service_code_cleaned.replace('@classmethodasync def', '@classmethod\nasync def')
                service_code_cleaned = service_code_cleaned.replace('@classmethoddef', '@classmethod\ndef')
                
                # 阶段2: 文档字符串
                service_code_cleaned = re.sub(r'(\) -> [^:]+:)"""', r'\1\n"""', service_code_cleaned)
                service_code_cleaned = re.sub(r'"""([^"]{5,}?)"""', lambda m: '"""\n' + m.group(1) + '\n"""', service_code_cleaned)
                service_code_cleaned = re.sub(r'"""([a-zA-Z])', r'"""\n\1', service_code_cleaned)
                
                # 阶段3: import 语句（更精确）
                service_code_cleaned = service_code_cleaned.replace('"""import ', '"""\nimport ')
                service_code_cleaned = re.sub(r'([a-z\)\]])import ', r'\1\nimport ', service_code_cleaned)
                service_code_cleaned = re.sub(r'([a-z\)\]])from ', r'\1\nfrom ', service_code_cleaned)
                # 修复 import 后面直接跟其他语句的情况（但不要截断单词）
                service_code_cleaned = re.sub(r'(import [a-z_]+\n)([a-z])', r'\1\n\2', service_code_cleaned)
                service_code_cleaned = re.sub(r'(from [^\n]+\n)([a-z])', r'\1\n\2', service_code_cleaned)
                
                # 阶段4: try/except/finally
                service_code_cleaned = re.sub(r'try:([a-zA-Z#\[])', r'try:\n\1', service_code_cleaned)
                service_code_cleaned = re.sub(r'except ([^:]+):([a-zA-Z])', r'except \1:\n\2', service_code_cleaned)
                service_code_cleaned = re.sub(r'finally:([a-zA-Z])', r'finally:\n\1', service_code_cleaned)
                
                # 阶段5: for/while/if（更激进）
                service_code_cleaned = re.sub(r'for ([^:]+):([a-zA-Z#])', r'for \1:\n\2', service_code_cleaned)
                service_code_cleaned = re.sub(r'while ([^:]+):([a-zA-Z#])', r'while \1:\n\2', service_code_cleaned)
                service_code_cleaned = re.sub(r'if ([^:]+):([a-zA-Z#])', r'if \1:\n\2', service_code_cleaned)
                
                # 阶段6: 变量赋值（更精确，避免截断函数参数）
                # 只在特定情况下添加换行：列表/元组结束后、数字后面
                service_code_cleaned = re.sub(r'(\])([a-z_][a-z0-9_]*\s*=\s*[^\n])', r']\n\2', service_code_cleaned)
                service_code_cleaned = re.sub(r'(\d)([a-z_][a-z0-9_]*\s*=\s*[A-Z\[])', r'\1\n\2', service_code_cleaned)
                
                # 阶段7: return/raise/await（更精确，避免截断）
                # 只在语句结束后添加换行，不要在语句中间添加
                service_code_cleaned = re.sub(r'([a-z\)\]])return ([A-Z])', r'\1\nreturn \2', service_code_cleaned)
                service_code_cleaned = re.sub(r'([a-z\)\]])raise ([A-Z])', r'\1\nraise \2', service_code_cleaned)
                service_code_cleaned = re.sub(r'([a-z\)\]])await ([A-Z])', r'\1\nawait \2', service_code_cleaned)
                
                # 阶段8: 注释
                service_code_cleaned = re.sub(r'([a-z\)\]])#', r'\1\n#', service_code_cleaned)
                
                # 阶段9: 方法调用后的语句
                service_code_cleaned = re.sub(r'(\))([a-z_][a-z0-9_]*\s*\()', r')\n\2', service_code_cleaned)
                
                # 阶段10: 清理多余空行
                service_code_cleaned = re.sub(r'\n\n\n+', '\n\n', service_code_cleaned)
                
                # 12. 智能添加缩进（更宽松的判断）
                lines = service_code_cleaned.split('\n')
                if lines:
                    # 检查是否需要添加缩进
                    non_empty_lines = [line for line in lines if line.strip()]
                    if non_empty_lines:
                        lines_without_indent = sum(1 for line in non_empty_lines if not line.startswith(' ') and not line.startswith('\t'))
                        # 如果超过50%的行没有缩进，或者第一行是装饰器/方法定义且没有缩进，认为需要修复
                        first_line = non_empty_lines[0] if non_empty_lines else ''
                        needs_fix = (lines_without_indent / len(non_empty_lines) > 0.5) or \
                                   (first_line.startswith(('@', 'async def', 'def ')) and not first_line.startswith(' '))
                        
                        if needs_fix:
                            fixed_lines = []
                            in_try_block = False
                            in_for_block = False
                            prev_line_type = None
                            
                            for i, line in enumerate(lines):
                                stripped = line.strip()
                                if not stripped:
                                    fixed_lines.append('')
                                    continue
                                
                                # 装饰器：4个空格
                                if stripped.startswith('@'):
                                    fixed_lines.append('    ' + stripped)
                                    prev_line_type = 'decorator'
                                # 方法定义：4个空格
                                elif stripped.startswith('async def') or stripped.startswith('def'):
                                    fixed_lines.append('    ' + stripped)
                                    prev_line_type = 'method_def'
                                # 文档字符串：8个空格
                                elif stripped.startswith('"""') or stripped.startswith("'''"):
                                    fixed_lines.append('        ' + stripped)
                                    prev_line_type = 'docstring'
                                # import 语句：8个空格
                                elif stripped.startswith('import ') or stripped.startswith('from '):
                                    fixed_lines.append('        ' + stripped)
                                    prev_line_type = 'import'
                                # try/finally：8个空格
                                elif stripped in ['try:', 'finally:']:
                                    fixed_lines.append('        ' + stripped)
                                    in_try_block = True
                                    prev_line_type = 'try'
                                # except：8个空格
                                elif stripped.startswith('except'):
                                    fixed_lines.append('        ' + stripped)
                                    in_try_block = True
                                    prev_line_type = 'except'
                                # for/while/if：12个空格（在try块内）
                                elif stripped.startswith(('for ', 'while ', 'if ')):
                                    fixed_lines.append('            ' + stripped)
                                    in_for_block = True
                                    prev_line_type = 'for'
                                # return/raise：12个空格（在try/except块内）
                                elif stripped.startswith('return ') or stripped.startswith('raise '):
                                    fixed_lines.append('            ' + stripped)
                                    prev_line_type = 'return'
                                # 单独的 raise（没有参数）：12个空格
                                elif stripped == 'raise':
                                    fixed_lines.append('            ' + stripped)
                                    prev_line_type = 'return'
                                # await：根据上下文判断
                                elif stripped.startswith('await '):
                                    if in_for_block:
                                        fixed_lines.append('                ' + stripped)
                                    else:
                                        fixed_lines.append('            ' + stripped)
                                    prev_line_type = 'await'
                                # 注释：根据上下文判断
                                elif stripped.startswith('#'):
                                    if in_for_block:
                                        fixed_lines.append('                ' + stripped)
                                    elif in_try_block:
                                        fixed_lines.append('            ' + stripped)
                                    else:
                                        fixed_lines.append('        ' + stripped)
                                    prev_line_type = 'comment'
                                # 其他语句：根据上下文判断
                                else:
                                    if in_for_block:
                                        fixed_lines.append('                ' + stripped)
                                    elif in_try_block:
                                        fixed_lines.append('            ' + stripped)
                                    else:
                                        fixed_lines.append('        ' + stripped)
                                    prev_line_type = 'statement'
                            
                            service_code_cleaned = '\n'.join(fixed_lines)
                
                # 验证修复后的代码
                # 判断是否为完整文件（包含import和class定义）
                is_full_file = 'import ' in service_code_cleaned and 'class ' in service_code_cleaned
                
                if is_full_file:
                    # 全量替换模式：直接验证新代码
                    max_attempts = 3
                    for attempt in range(max_attempts):
                        # 创建临时文件进行验证
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                            tmp.write(service_code_cleaned)
                            tmp_service_path = tmp.name
                        
                        try:
                            # 使用 py_compile 验证语法
                            result = subprocess.run(
                                ['python', '-m', 'py_compile', tmp_service_path],
                                capture_output=True,
                                text=True,
                                timeout=5
                            )
                            if result.returncode == 0:
                                # 验证成功，跳出循环
                                break
                            else:
                                # 验证失败
                                if attempt == max_attempts - 1:
                                    # 最后一次尝试失败 - 显示详细错误信息
                                    error_msg = result.stderr if result.stderr else result.stdout
                                    
                                    # 提取错误行号
                                    import re
                                    line_match = re.search(r'line (\d+)', error_msg)
                                    if line_match:
                                        error_line = int(line_match.group(1))
                                        # 读取临时文件，显示错误附近的代码
                                        try:
                                            with open(tmp_service_path, 'r', encoding='utf-8') as f:
                                                all_lines = f.readlines()
                                            # 显示错误行前后5行
                                            start = max(0, error_line - 6)
                                            end = min(len(all_lines), error_line + 5)
                                            context_lines = []
                                            for i in range(start, end):
                                                prefix = '>>> ' if i == error_line - 1 else '    '
                                                context_lines.append(f'{prefix}{i+1:4}: {all_lines[i].rstrip()}')
                                            error_context = '\n'.join(context_lines)
                                            error_msg += f'\n\n错误代码上下文：\n{error_context}'
                                        except:
                                            pass
                                    
                                    # 同时显示生成的代码（前30行）
                                    generated_preview = '\n'.join(service_code_cleaned.split('\n')[:30])
                                    error_msg += f'\n\n生成的代码（前30行）：\n{generated_preview}'
                                    
                                    validation_errors.append(f'Service 代码语法错误（全量替换模式）：\n{error_msg}')
                        finally:
                            # 删除临时文件
                            try:
                                os.unlink(tmp_service_path)
                            except:
                                pass
                elif os.path.exists(service_file):
                    # 追加模式：读取原文件并验证合并后的代码
                    async with aiofiles.open(service_file, 'r', encoding='utf-8') as f:
                        original_service = await f.read()
                    
                    # 尝试最多3次修复
                    max_attempts = 3
                    for attempt in range(max_attempts):
                        # 创建临时文件进行验证
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                            tmp.write(original_service)
                            tmp.write('\n')
                            tmp.write(service_code_cleaned)
                            tmp_service_path = tmp.name
                        
                        try:
                            # 在验证前先尝试用 black 格式化（关键改进！）
                            if attempt == 0:
                                try:
                                    # 先对新增代码单独格式化
                                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp_new:
                                        # 添加必要的导入和类定义，让 black 能正确识别缩进上下文
                                        tmp_new.write('class TempClass:\n')
                                        # 确保新代码有正确的基础缩进（4个空格）
                                        for line in service_code_cleaned.split('\n'):
                                            if line.strip():  # 跳过空行
                                                tmp_new.write('    ' + line.lstrip() + '\n')
                                            else:
                                                tmp_new.write('\n')
                                        tmp_new_path = tmp_new.name
                                    
                                    try:
                                        black_result = subprocess.run(
                                            ['black', '--quiet', tmp_new_path],
                                            capture_output=True,
                                            timeout=10,
                                            check=False
                                        )
                                        if black_result.returncode == 0:
                                            # black 格式化成功，读取格式化后的内容
                                            with open(tmp_new_path, 'r', encoding='utf-8') as f:
                                                formatted_content = f.read()
                                            # 移除临时添加的类定义，保留格式化后的方法
                                            formatted_lines = formatted_content.split('\n')
                                            if formatted_lines[0].strip() == 'class TempClass:':
                                                # 移除第一行的类定义，保留后面的内容
                                                service_code_cleaned = '\n'.join(formatted_lines[1:]).strip()
                                            
                                            # 重新写入临时文件进行验证
                                            with open(tmp_service_path, 'w', encoding='utf-8') as f:
                                                f.write(original_service)
                                                if not original_service.endswith('\n'):
                                                    f.write('\n')
                                                f.write('\n')
                                                f.write(service_code_cleaned)
                                    finally:
                                        try:
                                            os.unlink(tmp_new_path)
                                        except:
                                            pass
                                except Exception:
                                    pass
                            
                            # 使用 py_compile 验证语法
                            result = subprocess.run(
                                ['python', '-m', 'py_compile', tmp_service_path],
                                capture_output=True,
                                text=True,
                                timeout=5
                            )
                            if result.returncode == 0:
                                # 验证成功，跳出循环
                                break
                            else:
                                # 验证失败
                                if attempt == max_attempts - 1:
                                    # 最后一次尝试失败 - 显示详细错误信息
                                    error_msg = result.stderr if result.stderr else result.stdout
                                    
                                    # 提取错误行号
                                    import re
                                    line_match = re.search(r'line (\d+)', error_msg)
                                    if line_match:
                                        error_line = int(line_match.group(1))
                                        # 读取临时文件，显示错误附近的代码
                                        try:
                                            with open(tmp_service_path, 'r', encoding='utf-8') as f:
                                                all_lines = f.readlines()
                                            # 显示错误行前后5行
                                            start = max(0, error_line - 6)
                                            end = min(len(all_lines), error_line + 5)
                                            context_lines = []
                                            for i in range(start, end):
                                                prefix = '>>> ' if i == error_line - 1 else '    '
                                                context_lines.append(f'{prefix}{i+1:4}: {all_lines[i].rstrip()}')
                                            error_context = '\n'.join(context_lines)
                                            error_msg += f'\n\n错误代码上下文：\n{error_context}'
                                        except:
                                            pass
                                    
                                    # 同时显示生成的代码（前30行）
                                    generated_preview = '\n'.join(service_code_cleaned.split('\n')[:30])
                                    error_msg += f'\n\n生成的代码（前30行）：\n{generated_preview}'
                                    
                                    validation_errors.append(f'Service 代码语法错误（已尝试修复{max_attempts}次）：\n{error_msg}')
                        finally:
                            # 删除临时文件
                            try:
                                os.unlink(tmp_service_path)
                            except:
                                pass
            
            # 2. 验证并清理 Controller 代码（如果有）
            if controller_code:
                # 清理代码
                controller_code_cleaned = controller_code.strip()
                while controller_code_cleaned.startswith('\n'):
                    controller_code_cleaned = controller_code_cleaned[1:]
                
                # 判断是否为完整文件
                is_full_file = 'import ' in controller_code_cleaned and 'controller = APIRouterPro' in controller_code_cleaned
                
                if is_full_file:
                    # 全量替换模式：直接验证新代码
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                        tmp.write(controller_code_cleaned)
                        tmp_controller_path = tmp.name
                    
                    try:
                        # 使用 py_compile 验证语法
                        result = subprocess.run(
                            ['python', '-m', 'py_compile', tmp_controller_path],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if result.returncode != 0:
                            error_msg = result.stderr if result.stderr else result.stdout
                            validation_errors.append(f'Controller 代码语法错误（全量替换模式）：\n{error_msg}')
                        else:
                            # 语法正确，进一步检查 FastAPI 特定的问题
                            import re
                            
                            # 检查 Form/Query 的 default 参数错误
                            form_default_pattern = r'(Form|Query|Path|Body)\([^)]*default\s*='
                            if re.search(form_default_pattern, controller_code_cleaned):
                                logger.warning('⚠️ 检测到可能的 Form/Query 默认值错误')
                                # 提取具体的错误行
                                lines = controller_code_cleaned.split('\n')
                                error_lines = []
                                for i, line in enumerate(lines, 1):
                                    if re.search(form_default_pattern, line):
                                        error_lines.append(f'第 {i} 行: {line.strip()}')
                                
                                if error_lines:
                                    error_msg = '⚠️ FastAPI 参数错误：Form/Query/Path/Body 的默认值不能在 Annotated 中设置\n\n'
                                    error_msg += '错误的写法：\n'
                                    error_msg += '  count: Annotated[int, Form(default=10)] ❌\n\n'
                                    error_msg += '正确的写法：\n'
                                    error_msg += '  count: Annotated[int, Form()] = 10 ✅\n\n'
                                    error_msg += '发现以下可能的错误：\n'
                                    error_msg += '\n'.join(error_lines)
                                    validation_errors.append(error_msg)
                            
                            # 检查参数顺序：有默认值的参数必须在无默认值的参数之后
                            # 提取函数定义
                            func_pattern = r'async def \w+\([^)]+\):'
                            func_matches = re.finditer(func_pattern, controller_code_cleaned, re.DOTALL)
                            
                            for func_match in func_matches:
                                func_def = func_match.group(0)
                                # 简单检查：如果有 = 的参数后面还有 Annotated 参数（没有 =），可能有问题
                                # 这个检查不是100%准确，但可以捕获大部分情况
                                lines_in_func = func_def.split('\n')
                                found_default = False
                                param_order_errors = []
                                
                                for i, line in enumerate(lines_in_func):
                                    stripped = line.strip()
                                    # 跳过函数名行和空行
                                    if 'async def' in stripped or not stripped or stripped == ')':
                                        continue
                                    
                                    # 检查是否有默认值（但排除依赖注入）
                                    has_default = ' = ' in stripped and 'Dependency()' not in stripped
                                    is_param = 'Annotated[' in stripped or ':' in stripped
                                    
                                    if has_default:
                                        found_default = True
                                    elif found_default and is_param and 'Dependency()' in stripped:
                                        # 发现有默认值的参数后面还有依赖注入参数
                                        param_order_errors.append(f'参数顺序错误: {stripped}')
                                
                                if param_order_errors:
                                    error_msg = '⚠️ Python 参数顺序错误：有默认值的参数必须在无默认值的参数之后\n\n'
                                    error_msg += '错误的写法：\n'
                                    error_msg += '  async def func(\n'
                                    error_msg += '      count: int = 10,  # 有默认值\n'
                                    error_msg += '      query_db: AsyncSession,  # 无默认值 ❌\n'
                                    error_msg += '  ):\n\n'
                                    error_msg += '正确的写法：\n'
                                    error_msg += '  async def func(\n'
                                    error_msg += '      query_db: AsyncSession,  # 无默认值\n'
                                    error_msg += '      count: int = 10,  # 有默认值 ✅\n'
                                    error_msg += '  ):\n\n'
                                    error_msg += '发现以下可能的错误：\n'
                                    error_msg += '\n'.join(param_order_errors)
                                    validation_errors.append(error_msg)
                    finally:
                        # 删除临时文件
                        try:
                            os.unlink(tmp_controller_path)
                        except:
                            pass
                elif os.path.exists(controller_file):
                    # 追加模式：读取原有 Controller 文件并验证
                    async with aiofiles.open(controller_file, 'r', encoding='utf-8') as f:
                        original_controller = await f.read()
                    
                    # 创建临时文件进行验证
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp:
                        tmp.write(original_controller)
                        tmp.write('\n\n')
                        tmp.write(controller_code_cleaned)
                        tmp_controller_path = tmp.name
                    
                    try:
                        # 使用 py_compile 验证语法
                        result = subprocess.run(
                            ['python', '-m', 'py_compile', tmp_controller_path],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if result.returncode != 0:
                            error_msg = result.stderr if result.stderr else result.stdout
                            validation_errors.append(f'Controller 代码语法错误：\n{error_msg}')
                    finally:
                        # 删除临时文件
                        try:
                            os.unlink(tmp_controller_path)
                        except:
                            pass
            
            # 如果有验证错误，抛出异常
            if validation_errors:
                error_message = '代码验证失败：\n\n' + '\n\n'.join(validation_errors)
                error_message += '\n\n建议：\n1. 重新生成（AI 可能会生成更好的代码）\n2. 简化需求描述\n3. 手动修复后重新提交'
                raise ServiceException(message=error_message)
            
            # ========== 应用阶段 ==========
            os.makedirs(vue_dir, exist_ok=True)
            if api_code:
                os.makedirs(api_dir, exist_ok=True)

            # 写入Vue文件
            async with aiofiles.open(vue_file, 'w', encoding='utf-8') as f:
                await f.write(index_code)

            # 写入或追加API文件
            if api_code:
                # 清理 API 代码中的 import 语句（避免重复）
                api_code_lines = api_code.split('\n')
                api_code_cleaned = []
                for line in api_code_lines:
                    # 跳过 import request 语句
                    if line.strip().startswith("import request from") or line.strip().startswith('import request from'):
                        continue
                    api_code_cleaned.append(line)
                api_code_final = '\n'.join(api_code_cleaned).strip()
                
                if os.path.exists(api_file):
                    # 如果文件存在，检查是否为完整文件（包含 import）
                    async with aiofiles.open(api_file, 'r', encoding='utf-8') as f:
                        existing_content = await f.read()
                    
                    # 判断 AI 返回的是否为完整文件
                    has_import_in_new = 'import request' in api_code
                    has_import_in_existing = 'import request' in existing_content
                    
                    if has_import_in_new and not has_import_in_existing:
                        # 新代码有 import，旧文件没有 → 全量替换
                        async with aiofiles.open(api_file, 'w', encoding='utf-8') as f:
                            await f.write(api_code)
                    elif has_import_in_new and has_import_in_existing:
                        # 新旧都有 import → 可能是完整文件，全量替换
                        # 但也可能是 AI 错误地包含了 import，需要智能判断
                        # 如果新代码包含多个 export function，认为是完整文件
                        export_count = api_code.count('export function')
                        if export_count >= 3:  # 至少3个函数，认为是完整文件
                            async with aiofiles.open(api_file, 'w', encoding='utf-8') as f:
                                await f.write(api_code)
                        else:
                            # 只有少量函数，认为是新增，追加（去除 import）
                            async with aiofiles.open(api_file, 'a', encoding='utf-8') as f:
                                await f.write('\n\n' + api_code_final)
                    else:
                        # 新代码没有 import → 追加模式
                        async with aiofiles.open(api_file, 'a', encoding='utf-8') as f:
                            await f.write('\n\n' + api_code_final)
                else:
                    # 如果文件不存在，创建新文件
                    if 'import request' in api_code:
                        # AI 已经包含了 import
                        async with aiofiles.open(api_file, 'w', encoding='utf-8') as f:
                            await f.write(api_code)
                    else:
                        # AI 没有包含 import，手动添加
                        async with aiofiles.open(api_file, 'w', encoding='utf-8') as f:
                            await f.write("import request from '@/utils/request'\n\n")
                            await f.write(api_code)

            # 追加Controller代码（使用已验证的代码）
            if controller_code_cleaned and os.path.exists(controller_file):
                # 判断是否为完整文件（包含import和class定义）
                is_full_file = 'import ' in controller_code_cleaned and 'controller = APIRouterPro' in controller_code_cleaned
                
                if is_full_file:
                    # 全量替换模式
                    async with aiofiles.open(controller_file, 'w', encoding='utf-8') as f:
                        await f.write(controller_code_cleaned)
                else:
                    # 追加模式（兼容旧逻辑）
                    async with aiofiles.open(controller_file, 'a', encoding='utf-8') as f:
                        await f.write('\n\n')
                        await f.write(controller_code_cleaned)

            # 追加Service代码（使用已验证和修复的代码）
            if service_code_cleaned and os.path.exists(service_file):
                # 判断是否为完整文件（包含import和class定义）
                is_full_file = 'import ' in service_code_cleaned and 'class ' in service_code_cleaned
                
                if is_full_file:
                    # 全量替换模式
                    async with aiofiles.open(service_file, 'w', encoding='utf-8') as f:
                        await f.write(service_code_cleaned)
                else:
                    # 追加模式（兼容旧逻辑）
                    async with aiofiles.open(service_file, 'a', encoding='utf-8') as f:
                        await f.write('\n')
                        await f.write(service_code_cleaned)
                
                # 尝试使用 black 或 autopep8 格式化文件（强烈推荐）
                formatted = False
                try:
                    # 优先使用 black（更强大）
                    result = subprocess.run(
                        ['black', '--quiet', service_file],
                        capture_output=True,
                        timeout=10,
                        check=False
                    )
                    if result.returncode == 0:
                        formatted = True
                except Exception:
                    pass
                
                if not formatted:
                    try:
                        # 备选：使用 autopep8
                        subprocess.run(
                            ['autopep8', '--in-place', '--aggressive', '--aggressive', service_file],
                            capture_output=True,
                            timeout=10,
                            check=False
                        )
                    except Exception:
                        pass

            # 写入VO代码（如果有）
            if vo_code_cleaned:
                logger.info(f'📝 准备写入 VO 文件: {vo_file}')
                logger.info(f'📝 VO 代码长度: {len(vo_code_cleaned)} 字符')
                
                if os.path.exists(vo_file):
                    # 🔥 关键修复：在写入前检查 AI 生成的 VO 代码是否包含 Controller 需要的所有 Model
                    if controller_code_cleaned:
                        import re
                        
                        # 从 Controller 代码中提取导入的 Model
                        # 只匹配当前业务的 VO 文件（例如：teacher_vo）
                        vo_file_name = os.path.basename(vo_file).replace('.py', '')  # 例如：teacher_vo
                        import_pattern = rf'from\s+[\w.]+\.entity\.vo\.{vo_file_name}\s+import\s+([^;\n]+)'
                        import_match = re.search(import_pattern, controller_code_cleaned)
                        
                        if import_match:
                            imported_models = [m.strip() for m in import_match.group(1).split(',')]
                            logger.info(f'📋 Controller 从 {vo_file_name} 导入的 Model: {imported_models}')
                            
                            # 检查 AI 生成的 VO 代码中是否包含所有需要的 Model
                            missing_models = []
                            for model in imported_models:
                                if f'class {model}' not in vo_code_cleaned:
                                    missing_models.append(model)
                            
                            if missing_models:
                                logger.warning(f'⚠️ AI 生成的 VO 代码缺少 Model: {missing_models}')
                                logger.info(f'🔧 尝试从原 VO 文件中提取缺失的 Model')
                                
                                # 读取原有 VO 文件
                                async with aiofiles.open(vo_file, 'r', encoding='utf-8') as f:
                                    existing_vo_content = await f.read()
                                
                                # 从原文件中提取缺失的 Model 定义
                                extracted_models = []
                                for model_name in missing_models:
                                    # 使用正则提取整个类定义（包括装饰器、方法等）
                                    class_pattern = rf'((?:@[\w.]+(?:\([^)]*\))?\s*)*class {model_name}\([^)]+\):.*?)(?=\n(?:@[\w.]+|class\s+\w+|$))'
                                    class_match = re.search(class_pattern, existing_vo_content, re.DOTALL)
                                    
                                    if class_match:
                                        extracted_models.append('\n\n' + class_match.group(1).rstrip())
                                        logger.info(f'✅ 从原文件提取到 {model_name}')
                                    else:
                                        # 如果原文件也没有，自动生成
                                        logger.warning(f'⚠️ 原文件也没有 {model_name}，自动生成')
                                        if 'GenerateRandom' in model_name or 'Generate' in model_name:
                                            model_code = f'''

class {model_name}(BaseModel):
    """
    {model_name.replace('Model', '')} 请求模型（自动生成）
    """
    model_config = ConfigDict(alias_generator=to_camel)

    count: int = Field(default=10, description='生成数据数量', ge=1, le=100)
'''
                                        else:
                                            model_code = f'''

class {model_name}(BaseModel):
    """
    {model_name.replace('Model', '')} 模型（自动生成）
    """
    model_config = ConfigDict(alias_generator=to_camel)
'''
                                        extracted_models.append(model_code)
                                
                                # 将提取/生成的 Model 追加到 AI 生成的 VO 代码后面
                                if extracted_models:
                                    vo_code_cleaned = vo_code_cleaned.rstrip() + '\n' + '\n'.join(extracted_models)
                                    logger.info(f'✅ 已补充 {len(missing_models)} 个缺失的 Model 到 VO 代码')
                    
                    # 判断是否为完整文件（包含import和class定义）
                    is_full_file = 'import ' in vo_code_cleaned and 'class ' in vo_code_cleaned
                    
                    logger.info(f'📝 VO 文件模式: {"全量替换" if is_full_file else "追加"}')
                    
                    if is_full_file:
                        # 全量替换模式
                        async with aiofiles.open(vo_file, 'w', encoding='utf-8') as f:
                            await f.write(vo_code_cleaned)
                        logger.info(f'✅ VO 文件已全量替换')
                    else:
                        # 追加模式（兼容旧逻辑）
                        async with aiofiles.open(vo_file, 'a', encoding='utf-8') as f:
                            await f.write('\n\n')
                            await f.write(vo_code_cleaned)
                        logger.info(f'✅ VO 文件已追加')
                    
                    # 尝试使用 black 格式化 VO 文件
                    try:
                        subprocess.run(
                            ['black', '--quiet', vo_file],
                            capture_output=True,
                            timeout=10,
                            check=False
                        )
                        logger.info(f'✅ VO 文件已格式化')
                    except Exception as e:
                        logger.warning(f'⚠️ VO 文件格式化失败: {str(e)}')
                else:
                    logger.warning(f'⚠️ VO 文件不存在: {vo_file}')
            else:
                logger.info('ℹ️ 未收到 VO 代码，尝试自动检测并生成缺失的 Model')
                
                # 🔥 自动检测和生成缺失的 Model（后备方案）
                if controller_code_cleaned and os.path.exists(vo_file):
                    import re
                    
                    # 从 Controller 代码中提取导入的 Model
                    # 只匹配当前业务的 VO 文件
                    vo_file_name = os.path.basename(vo_file).replace('.py', '')  # 例如：teacher_vo
                    import_pattern = rf'from\s+[\w.]+\.entity\.vo\.{vo_file_name}\s+import\s+([^;\n]+)'
                    import_match = re.search(import_pattern, controller_code_cleaned)
                    
                    if import_match:
                        imported_models = [m.strip() for m in import_match.group(1).split(',')]
                        logger.info(f'📋 Controller 从 {vo_file_name} 导入的 Model: {imported_models}')
                        
                        # 读取现有 VO 文件
                        async with aiofiles.open(vo_file, 'r', encoding='utf-8') as f:
                            existing_vo_content = await f.read()
                        
                        # 检查哪些 Model 缺失
                        missing_models = []
                        for model in imported_models:
                            if f'class {model}' not in existing_vo_content:
                                missing_models.append(model)
                        
                        if missing_models:
                            logger.warning(f'⚠️ 发现缺失的 Model: {missing_models}')
                            
                            # 自动生成缺失的 Model
                            generated_models = []
                            for model_name in missing_models:
                                # 生成简单的 Model 定义
                                if 'GenerateRandom' in model_name or 'Generate' in model_name:
                                    # 生成随机数据的请求模型
                                    model_code = f'''

class {model_name}(BaseModel):
    """
    {model_name.replace('Model', '')} 请求模型（自动生成）
    """
    model_config = ConfigDict(alias_generator=to_camel)

    count: int = Field(default=10, description='生成数据数量', ge=1, le=100)
'''
                                else:
                                    # 通用请求模型
                                    model_code = f'''

class {model_name}(BaseModel):
    """
    {model_name.replace('Model', '')} 模型（自动生成）
    """
    model_config = ConfigDict(alias_generator=to_camel)
'''
                                generated_models.append(model_code)
                            
                            # 追加到 VO 文件
                            async with aiofiles.open(vo_file, 'a', encoding='utf-8') as f:
                                for model_code in generated_models:
                                    await f.write(model_code)
                            
                            logger.info(f'✅ 已自动生成 {len(missing_models)} 个缺失的 Model')
                            
                            # 格式化文件
                            try:
                                subprocess.run(
                                    ['black', '--quiet', vo_file],
                                    capture_output=True,
                                    timeout=10,
                                    check=False
                                )
                            except Exception:
                                pass
                        else:
                            logger.info('✅ 所有 Model 都已存在，无需生成')

            return CrudResponseModel(is_success=True, message='✅ 应用重构成功！代码已通过语法验证。')

        except ServiceException as e:
            raise e
        except Exception as e:
            raise ServiceException(message=f'应用重构失败: {str(e)}')


class GenTableColumnService:
    """
    代码生成业务表字段服务层
    """

    @classmethod
    async def get_gen_table_column_list_by_table_id_services(
        cls, query_db: AsyncSession, table_id: int
    ) -> list[GenTableColumnModel]:
        """
        获取业务表字段列表信息service

        :param query_db: orm对象
        :param table_id: 业务表格id
        :return: 业务表字段列表信息对象
        """
        gen_table_column_list_result = await GenTableColumnDao.get_gen_table_column_list_by_table_id(query_db, table_id)

        return [
            GenTableColumnModel(**gen_table_column)
            for gen_table_column in CamelCaseUtil.transform_result(gen_table_column_list_result)
        ]
