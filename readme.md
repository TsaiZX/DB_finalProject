# DataBase final project template

## Flask + PostgreSQL
    Creater Database 
    run app.py to start the server
    then Running on http://127.0.0.1:5000

## Base function
- Insert : insert new data to specific table
- Delete : delete data from specific table
- Modify : modify data
- search : search table

## Possible problems and Solution
- Permission denied for relation : GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO 'someuser';

- FATAL: password authentication failed for user : 編輯 postgreSQL 目錄下的 pg_hba.conf ,將 md5 認證修改成 trust 認證，編輯後退出儲存
