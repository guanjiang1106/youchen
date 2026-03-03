@echo off
echo Migrating database...
docker exec -i ruoyi-pg psql -U postgres -d ruoyi-fastapi -c "ALTER TABLE gen_table ADD COLUMN IF NOT EXISTS form_layout VARCHAR(5000) NULL;"
docker exec -i ruoyi-pg psql -U postgres -d ruoyi-fastapi -c "COMMENT ON COLUMN gen_table.form_layout IS 'Form layout config in JSON format';"
echo Migration completed!
pause
