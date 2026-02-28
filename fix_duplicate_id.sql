-- 修复 gen_table_column 表中重复的 id 字段
-- 在数据库中执行此 SQL

-- 1. 查看 material 表的字段配置（检查是否有重复）
SELECT gc.column_id, gc.column_name, gc.is_pk, gc.sort, gc.table_id
FROM gen_table_column gc
JOIN gen_table gt ON gc.table_id = gt.table_id
WHERE gt.table_name = 'material'
ORDER BY gc.sort;

-- 2. 删除重复的 id 字段（保留 sort 最小的那个）
DELETE FROM gen_table_column 
WHERE column_id IN (
  SELECT gc.column_id 
  FROM gen_table_column gc
  JOIN gen_table gt ON gc.table_id = gt.table_id
  WHERE gt.table_name = 'material' 
    AND gc.column_name = 'id'
    AND gc.column_id NOT IN (
      SELECT MIN(gc2.column_id) 
      FROM gen_table_column gc2
      JOIN gen_table gt2 ON gc2.table_id = gt2.table_id
      WHERE gt2.table_name = 'material' 
        AND gc2.column_name = 'id'
    )
);

-- 3. 重新排序字段（可选）
WITH numbered_columns AS (
  SELECT gc.column_id, 
         ROW_NUMBER() OVER (PARTITION BY gc.table_id ORDER BY gc.sort) as new_sort
  FROM gen_table_column gc
  JOIN gen_table gt ON gc.table_id = gt.table_id
  WHERE gt.table_name = 'material'
)
UPDATE gen_table_column gc
SET sort = nc.new_sort
FROM numbered_columns nc
WHERE gc.column_id = nc.column_id;

-- 4. 验证修复结果
SELECT gc.column_id, gc.column_name, gc.is_pk, gc.sort
FROM gen_table_column gc
JOIN gen_table gt ON gc.table_id = gt.table_id
WHERE gt.table_name = 'material'
ORDER BY gc.sort;
