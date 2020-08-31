# Flask Quickstart

## 1. 介绍

Flask Quickstart 是一个具有 Web 后端基本功能、易于快读二次开发的 Flask 项目。

## 2. 特性

- 界面和接口，所有功能接口化
- 权限控制，用户、模块、权限三维控制
- 访问统计，记录所有非匿名访问请求
- 运维日志，文件日志和错误邮件
- 语言本地化，集成 babel
- 单元测试，得到测试覆盖率报告
- 接口文档，文档和代码合于一处，项目启动后访问 `/docs/api`
- [开发文档](docs/README.md)，各类文档丰富
- Docker 部署

## 3. 结构

- `app`：源代码
  - `api`：api 蓝图，只用于注册端点，实现分散到各个模块的 api
  - `auth`：用户认证，只用于界面验证，api 用户认证在 `api/tokens.py`
  - `beans`：业务模型
  - `errors`：错误处理
  - `main`：用户管理
  - `static`：静态资源
  - `templates`：jinja2 模版
  - `translations`：本地化资源
  - `utils`：工具函数
  - `__init__.py`：应用程序创建函数
  - `models.py`：系统模型，业务模型放到 `app/beans`
- `.env`：配置文件，应用程序启动前必须具备！
- `.env.template`：配置文件模版
- `data`：数据等，应用程序运行时产生的临时缓存数据放到 `tmp`
- `docs`：开发者文档
- `log`: 日志
- `migrations`：数据库迁移记录
- `scripts`：脚本
- `tests`：单元测试
- `tmp`：临时缓存数据
- `config.py`：配置加载脚本
- `flask_quickstart.py`：启动脚本

## 4. 部署

### 4.1. 配置数据库

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

> 开发者执行 SQL 脚本 `scripts/create_database_and_user.sql`

1. 修改 `/etc/mysql/mysql.conf.d/mysqld.cnf` 中为：`bind-address = 0.0.0.0`
2. 从 `/etc/mysql/mysql.conf.d/mysqld.cnf` 中还可以获知数据库端口，默认：`3306`
3. 重启 mysql 服务 `service mysql restart`
4. 验证 mysql 服务 `netstat -tnl | grep 3306` ，出现 `0.0.0.0:3306` , `:::3306`, `LISTEN` 类似字符，说明数据库运行正常。

### 4.2. 启动容器

```bash
# 构建镜像
docker build -t flask_quickstart_web:<tag> .
```

```bash
docker run -itd --name=flask_quickstart_web_app -p 8080:8080 \
  -v /repo_path:/opt/flask-quickstart \
  flask_quickstart_web:<tag> /bin/bash
```

```bash
docker exec -it flask_quickstart_web_app /bin/bash
```

### 4.3. 容器内部操作

> 该节内容执行后效果等同于运行 `boot.sh`

```bash
cd /opt/flask-quickstart
cp .env.template .env
vim .env
```

```properties
SECRET_KEY=a_random_and_long_string
DB_SERVER=172.17.0.1
DB_PORT=3306
DB_USERNAME=www
DB_PASSWORD=password
DB_DATABASE=flaskqs
DB_DATABASE_TEST=
MAIL_SERVER=
MAIL_PORT=
MAIL_USE_SSL=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_ADMINS=
```

根据需要修改 .env 文件

- 执行 `python -c "import uuid; print(uuid.uuid4().hex)"` ，粘贴到 `SECRET_KEY`
- `172.17.0.1` 为 docker 网桥中宿主机默认 ip，其他 `DB` 信息根据需要修改
- `MAIL` 信息配置可参见 [邮箱配置](docs/mail.md)

```bash
# 数据库升级
# 执行前提：创建好数据库和配置 .env 文件
# 执行效果：生成数据库表结构
flask db upgrade
```

```bash
# 编译 web 后端界面的本地化文件
# 执行效果：后端界面变成全中文
flask translate compile
```

```bash
# 启动 supervisor 服务
cp supervisor.conf /etc/supervisor/conf.d/flask_quickstart.conf
service supervisor start
# 启动 nginx 服务
rm /etc/nginx/sites-enabled/default
cp nginx.conf /etc/nginx/sites-enabled/
service nginx start
```

### 4.4. 验证运行情况

> 验证方法均在容器内部进行。方法选其一即可。

#### 4.4.1. 端口监听

```bash
netstat -tnl
```

- 出现 `127.0.0.1:8000` , `LISTEN` 类似字符，说明 web 后端程序运行正常。
- 出现 `0.0.0.0:8080` , `:::8080`, `LISTEN` 类似字符，说明 nginx 运行正常。

#### 4.4.2. 服务状态

```bash
service supervisor status
# supervisord is running
```

说明 web 后端程序运行正常。

```bash
service nginx status
# [ ok ] Starting nginx: nginx.
```

说明 nginx 运行正常。
