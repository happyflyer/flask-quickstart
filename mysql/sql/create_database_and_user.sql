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
