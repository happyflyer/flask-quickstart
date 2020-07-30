-- create database
drop database if exists `flaskqs`;
create database `flaskqs` character set 'utf8' collate 'utf8_general_ci';
-- drop database if exists `flaskqs_test`;
-- create database `flaskqs_test` character set 'utf8' collate 'utf8_general_ci';
-- create user
create user 'www' @'localhost' identified by 'password';
grant all privileges on flaskqs.* to 'www' @'localhost';
-- grant all privileges on flaskqs_test.* to 'www'@'localhost';
flush privileges;
-- all user
-- select host, user, authentication_string from mysql.user;
-- grant www
-- show grants for www@localhost;