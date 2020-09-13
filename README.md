# Flask Quickstart

## 1. 介绍

Flask Quickstart 是一个具有 Web 后端基本功能、易于快读二次开发的 Flask 项目。

## 2. 特性

- 界面和接口
- 权限控制
- 访问日志
- 运维日志
- [语言本地化](docs/flask.md)
- [单元测试](docs/test.md)
- 接口文档
- [开发文档](docs/README.md)
- Docker 部署

## 3. 结构

- `app`：源代码
  - `api`：api 蓝图，只有 api 的基础配置，实现在各模块的 api 文件夹
  - `auth`：用户认证，只用于界面认证，api 的认证在 `api/tokens.py`
  - `beans`：业务模型
  - `errors`：错误处理，处理 4xx 和 5xx 错误
  - `main`：主模块，包括首页、用户管理等
  - `static`：静态资源
  - `templates`：jinja2 模版
  - `translations`：本地化资源
  - `utils`：工具函数
  - `__init__.py`：应用工厂函数
  - `models.py`：系统模型，业务模型放到 `app/beans`
- `.env.template`：配置文件模版
- `data`：相对固定的数据，应用程序运行时产生的缓存数据放到 `tmp`
- `docs`：开发者文档
- `log`：错误日志
- `migrations`：数据库迁移记录
- `scripts`：各种脚本
- `tests`：单元测试
- `tmp`：缓存数据
- `config.py`：用于加载配置文件
- `main.py`：用于启动应用程序

## 4. 部署

### 4.1. 配置数据库

```bash
mysql -u root -p
```

```sql
-- 创建数据库
drop database if exists flaskqs;
create database flaskqs character set 'utf8' collate 'utf8_general_ci';
-- 创建用户
create user 'www' @'%' identified by 'password';
-- 授权
grant all privileges on flaskqs.* to 'www' @'%';
flush privileges;
```

1. 修改 `/etc/mysql/mysql.conf.d/mysqld.cnf` 中为：`bind-address = 0.0.0.0`
2. 从 `/etc/mysql/mysql.conf.d/mysqld.cnf` 中还可以获知数据库端口，默认：`3306`
3. 重启 mysql 服务 `service mysql restart`
4. 验证 mysql 服务 `netstat -tnl | grep 3306` ，出现 `0.0.0.0:3306` , `:::3306`, `LISTEN` 类似字符，说明数据库运行正常。

### 4.2. 配置文件

```bash
cp .env.template .env
```

```vim
APP_NAME=Flask Quickstart
SECRET_KEY=a_random_and_long_string
DB_SERVER=
DB_PORT=3306
DB_USERNAME=www
DB_PASSWORD=
DB_DATABASE=flaskqs
DB_DATABASE_TEST=
MAIL_SERVER=
MAIL_PORT=
MAIL_USE_SSL=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_ADMINS=
```

### 4.3. 启动容器

```bash
chmod +x boot.sh
# 创建容器
docker run -itd --name=flask_quickstart_container -p 8080:8080 --restart=always \
  -v /repo_path:/opt/flask-quickstart \
  flask_quickstart_image /opt/flask-quickstart/boot.sh
```

### 4.4. 验证运行情况

> 验证方法均在容器内部进行。方法选其一即可。

```bash
# 进入容器
docker exec -it flask_quickstart_container /bin/bash
```

#### 4.4.1. 端口监听

```bash
netstat -tnl
```

- 出现 `127.0.0.1:8000` , `LISTEN` 类似字符，说明 web 后端程序运行正常。
- 出现 `0.0.0.0:8080` , `:::8080`, `LISTEN` 类似字符，说明 nginx 运行正常。

#### 4.4.2. 服务状态

```bash
service supervisor status
# 执行效果：supervisord is running
```

```bash
service nginx status
# 执行效果：[ ok ] nginx is running.
```
