-- 修复 list_column 视图，避免重复字段
-- 在数据库中执行此 SQL

DROP VIEW IF EXISTS list_column;

CREATE OR REPLACE VIEW list_column AS
SELECT DISTINCT ON (c.relname, a.attname)
       c.relname                                                                           AS table_name,
       a.attname                                                                           AS column_name,
       d.description                                                                       AS column_comment,
       CASE
           WHEN a.attnotnull AND con.conname IS NULL THEN '1'
           ELSE '0'
           END                                                                             AS is_required,
       CASE
           WHEN con.contype = 'p' THEN '1'  -- 只判断主键约束
           ELSE '0'
           END                                                                             AS is_pk,
       a.attnum                                                                            AS sort,
       CASE
           WHEN "position"(pg_get_expr(ad.adbin, ad.adrelid), ((c.relname::text || '_'::text) || a.attname
                           ::text) || '_seq'::text) > 0 THEN '1'
           ELSE '0'
           END                                                                             AS is_increment,
       btrim(
                   CASE
                       WHEN t.typelem <> 0::oid AND t.typlen = '-1'::integer THEN 'ARRAY'::text
            ELSE
            CASE
                WHEN t.typtype = 'd'::"char" THEN format_type(t.typbasetype, NULL::integer)
                ELSE format_type(a.atttypid, NULL::integer)
            END
        END, '"'::text) AS column_type
FROM pg_attribute a
         JOIN (pg_class c
    JOIN pg_namespace n ON c.relnamespace = n.oid) ON a.attrelid = c.oid
         LEFT JOIN pg_description d ON d.objoid = c.oid AND a.attnum = d.objsubid
         LEFT JOIN pg_constraint con ON con.conrelid = c.oid AND (a.attnum = ANY (con.conkey)) AND con.contype = 'p'  -- 只关联主键约束
         LEFT JOIN pg_attrdef ad ON a.attrelid = ad.adrelid AND a.attnum = ad.adnum
         LEFT JOIN pg_type t ON a.atttypid = t.oid
WHERE (c.relkind = ANY (ARRAY['r'::"char", 'p'::"char"]))
  AND a.attnum > 0
  AND n.nspname = 'public'::name
  AND NOT a.attisdropped
ORDER BY c.relname, a.attname, a.attnum;
