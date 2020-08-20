-- 创建数据库，数据库名根据需要设置
drop database if exists `flaskqs`;
create database `flaskqs` character set 'utf8' collate 'utf8_general_ci';
-- 开发者如需进行单元测试，必须创建测试数据库
drop database if exists `flaskqs_test`;
create database `flaskqs_test` character set 'utf8' collate 'utf8_general_ci';
-- 创建用户，用户名和密码根据需要设置
create user 'www' @'%' identified by 'password';
-- 给用户授权
grant all privileges on flaskqs.* to 'www' @'%';
grant all privileges on flaskqs_test.* to 'www' @'%';
flush privileges;
-- 验证用户和授权
-- select host, user, authentication_string from mysql.user;
-- show grants for 'www'@'%';