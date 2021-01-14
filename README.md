# flask-quickstart

## 1. 安装依赖

```bash
conda create -n flask_quickstart_venv python=3.6
conda activate flask_quickstart_venv
pip install -r requirements.txt
```

## 2. 创建数据库

```sql
-- 创建数据库 flask_quickstart
drop database if exists flask_quickstart;
create database flask_quickstart character set 'utf8' collate 'utf8_general_ci';
-- 创建用户 flask_quickstart 并授权
create user 'flask_quickstart'@'%' identified by 'MySQL@flask_quickstart123456';
grant all privileges on flask_quickstart.* to 'flask_quickstart'@'%';
flush privileges;
-- 开发环境下还需要创建测试数据库 flask_quickstart_test
-- drop database if exists flask_quickstart_test;
-- create database flask_quickstart_test character set 'utf8' collate 'utf8_general_ci';
-- grant all privileges on flask_quickstart_test.* to 'flask_quickstart'@'%';
-- flush privileges;
-- 查询 MySQL 的所有用户
-- select host, user, authentication_string from mysql.user;
-- 查看用户 flask_quickstart 的权限
-- show grants for 'flask_quickstart'@'%';
```

## 3. 修改配置文件

```bash
cp .env.template .env
```

```properties
# .env
APP_NAME=flask-quickstart
SECRET_KEY=a_random_and_long_string
DB_SERVER=localhost
DB_PORT=3306
DB_USERNAME=flask_quickstart
DB_PASSWORD=MySQL@flask_quickstart123456
DB_DATABASE=flask_quickstart
DB_DATABASE_TEST=flask_quickstart_test
MAIL_SERVER=
MAIL_PORT=
MAIL_USE_SSL=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_ADMINS=
```

```properties
# .flaskenv
FLASK_APP=main.py
FLASK_ENV=development
# FLASK_ENV=production
```

## 4. 执行表结构迁移

```bash
# flask db init
# flask db migrate -m "create tables"
flask db upgrade
```

## 5. 编译翻译文本

```bash
# flask translate init zh
# flask translate update
flask translate compile
```

## 6. 启动调试

```bash
flask run
```

```bash
flask run -h 0.0.0.0 -p 8000
```

```bash
flask shell
```

```bash
flask routes
```
