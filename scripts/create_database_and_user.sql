-- 创建数据库
drop database if exists flaskqs;
create database flaskqs character
set 'utf8' collate 'utf8_general_ci';
-- 创建测试数据库
drop database if exists flaskqs_test;
create database flaskqs_test character
set 'utf8' collate 'utf8_general_ci';
-- 创建用户
drop user 'www' @'%';
create user 'www' @'%' identified by 'password';
flush privileges;
-- 授权
grant all privileges on flaskqs.* to 'www' @'%';
grant all privileges on flaskqs_test.* to 'www' @'%';
flush privileges;
-- 查询用户
select host,
    user,
    authentication_string
from mysql.user;
-- 查询授权
show grants for 'www' @'%';