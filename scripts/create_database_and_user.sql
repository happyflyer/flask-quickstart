-- 创建数据库
drop database if exists flask_quickstart_db;
create database flask_quickstart_db character set 'utf8' collate 'utf8_general_ci';
-- 创建用户并授权
create user 'www' @'%' identified by 'MySQL@www123456';
grant all privileges on flask_quickstart_db.* to 'www' @'%';
flush privileges;
-- 查询用户
-- select host, user, authentication_string from mysql.user;
-- 查询授权
-- show grants for 'www' @'%';