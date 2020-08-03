# Flask Quickstart

## 1. 介绍

Flask Quickstart 是一个具有 Web 后端基本功能、易于快读二次开发的 Flask 项目。

## 2. 特点

- 界面和接口，所有功能接口化
- 权限控制，用户、模块、权限三维控制
- 访问统计，记录所有非匿名访问请求
- 运维日志，文件日志和错误邮件
- 语言本地化，集成 babel
- 单元测试，得到测试覆盖率报告
- 接口文档，文档和代码合于一处，项目启动后访问 `/docs/api`
- [开发文档](docs/README.md)，各类文档丰富
- Docker 部署

## 3. 部署

### 3.1. 配置数据库

```bash
mysql -u root -p
```

```sql
-- 创建数据库，数据库名根据需要设置
drop database if exists `flaskqs`;
create database `flaskqs` character set 'utf8' collate 'utf8_general_ci';
-- 创建用户，用户名和密码根据需要设置
create user 'www' @'%' identified by 'password';
-- 给用户授权
grant all privileges on flaskqs.* to 'www' @'%';
flush privileges;
```

1. 修改 `/etc/mysql/mysql.conf.d/mysqld.cnf` 中为：`bind-address = 0.0.0.0`
2. 从 `/etc/mysql/mysql.conf.d/mysqld.cnf` 中还可以获知数据库端口，默认：`3306`
3. 重启 mysql 服务 `service mysql restart`
4. 验证 mysql 服务 `netstat -tnl | grep 3306` ，出现 `0.0.0.0:3306` 和 `LISTEN` 说明运行正常。

### 3.2. 启动容器

```bash
# 构建镜像
docker build -t flaskqs:<tag> .
```

```bash
docker run -itd -p 8080:8080 flaskqs:<tag> /bin/bash
```

```bash
docker ps
docker exec -it <container_id> /bin/bash
```

### 3.3. 配置 .env

```bash
cp .env.template .env
```

```properties
SECRET_KEY=a_random_and_long_string
DB_SERVER=172.17.0.1
DB_PORT=3306
DB_USERNAME=www
DB_PASSWORD=password
DB_DATABASE=flaskqs
DB_DATABASE_TEST=flaskqs_test
MAIL_SERVER=smtp.qq.com
MAIL_PORT=<465或者587>
MAIL_USE_SSL=1
MAIL_USERNAME=<qq账号>
MAIL_PASSWORD=<qq邮箱授权码>
MAIL_ADMINS=<邮箱，多个邮箱之间用','分隔>
```

- 执行 `python -c "import uuid; print(uuid.uuid4().hex)"` ，粘贴到 `SECRET_KEY`
- `172.17.0.1` 为 docker 网桥中宿主机默认 ip，其他 `DB` 信息根据需要修改
- `MAIL` 信息配置可参见 [邮箱配置](docs/mail.md)

### 3.4. 启动服务

```bash
flask db upgrade
```

```bash
flask translate compile
```

```bash
service supervisor start
service nginx start
```
