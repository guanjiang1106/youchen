@classmethod
    async def generate_random_teacher_services(cls, query_db: AsyncSession, count: int) -> CrudResponseModel:
        """随机生成老师维护信息"""
        import random
        
        try:
            teachers = []
            for i in range(count):
                teacher = TeacherModel(name=f'Teacher{i}')
                teachers.append(teacher)
            
            await TeacherDao.add_teacher_dao(query_db, teacher)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='成功')
        except Exception as e:
            await query_db.rollback()
            raise e