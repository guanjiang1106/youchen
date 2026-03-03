    @classmethod
    async def generate_random_teacher_services(cls, query_db: AsyncSession, count: int) -> CrudResponseModel:
        """
        随机生成老师维护信息 service:param query_db: orm 对象:param count: 生成数量:return: 随机生成老师维护校验结果
        """
        import rando
        m
        from datetime import datetime, timedeltatry:
        # 定义随机数据源departments = ['计算机学院', '数学学院', '物理学院', '化学学院', '生物学院', '文学院', '历史学院', '哲学学院']
        titles = ['讲师', '副教授', '教授', '助教', '研究员']
        gender_values = [0, 1]
        status_values = [0, 1]
        teachers = []
        base_date = datetime.now() - timedelta(days=365 * 20)for i in range(count):
        # 生成随机数据first_name = random.choice(['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴'])
        last_name = random.choice(['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋'])
        name = f'{first_name}{last_name}'teacher_no = f"T{datetime.now().strftime('%Y%m%d%H%M%S')}{str(i).zfill(3)}"gender = random.choice(gender_values)
        birth_date = base_date + timedelta(days=random.randint(0, 365 * 40))
        phone = f'1{random.randint(3, 9)}{random.randint(100000000, 999999999)}'email = f'{name.lower()}{random.randint(1, 999)}@example.com'department = random.choice(departments)
        title = random.choice(titles)
        status = random.choice(status_values)
        teacher = TeacherModel(teacher_no=teacher_no,name=name,gender=gender,birth_date=birth_date.strftime('%Y-%m-%d'),phone=phone,email=email,department=department,title=title,status=status,create_time=datetime.now(),update_time=datetime.now(),)teachers.append(teacher)
        # 批量插入for teacher in teachers:
        await TeacherDao.add_teacher_dao(query_db, teacher)
        await query_db.commit()
        return CrudResponseModel(is_success=True, message=f'成功生成{count}条随机数据')except Exception as e:
        await query_db.rollback()
        raise
        e