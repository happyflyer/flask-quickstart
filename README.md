# flask-quickstart

## 1. 项目特色

项目只提供 Flask 项目的基本框架和功能，包括：

- 用户认证
- 权限控制
- 访问记录
- 定时任务
- 单元测试
- Docker 部署
- ...

基于本项目开发的 Flask 程序，可以实现业务功能最大程度的定制化。

## 2. 文件结构

```bash
.
├── app
│   ├── api
│   │   ├── auth.py  # api 认证处理函数
│   │   ├── basedata_api.py  # 基础数据的 api
│   │   ├── errors.py  # api 错误处理函数
│   │   ├── test_api.py  # 测试接口的 api
│   │   └── token_api.py  # 用户认证的 api
│   ├── auth
│   │   ├── forms.py  # 页面认证表单
│   │   └── routes.py  # 页面认证路由
│   ├── beans  # 业务模型
│   ├── errors
│   │   └── handlers.py  # app 全局错误处理函数
│   ├── main
│   │   ├── api
│   │   │   └── user_api.py  # 用户管理的 api
│   │   ├── forms.py  # 用户管理表单
│   │   ├── routes.py  # index 路由
│   │   └── user_view.py  # 用户管理理由
│   ├── static  # 静态资源
│   ├── templates  # jijia2 模板
│   ├── translations  # 本地化翻译文本
│   ├── utils
│   │   ├── dt.py  # 日期时间处理
│   │   ├── io.py  # 文本文件读写
│   │   └── string.py  # 字符串处理
│   ├── __init__.py  # 应用工厂函数
│   ├── apscheduler.py  # 解决多进程中APScheduler重复运行的问题
│   ├── cli.py  # 自定义命令
│   ├── database.py  # 数据库初始化
│   ├── email.py  # 发送电子邮件
│   ├── jobs.py  # 设置定时人物
│   ├── models.py  # 系统模型
│   ├── modules.py  # 注册功能模块
│   ├── momentjs.py  # 日期时间本地化
│   ├── page.py  # 分页参数
│   └── permission.py  # 访问权限控制
├── config
│   ├── docker-compose.yml  # 部署 Docker 启动
│   ├── nginx.conf  # 部署 nginx 配置
│   └── supervisor.conf  # 部署 supervisor 配置
├── data  # 元数据
├── docker  # 运行时 Docker 镜像构建
├── migrations  # 数据库表结构迁移
├── mysql  # mysql 容器启动
├── scripts
│   ├── clean_pycache.sh  # 清理 pyc 脚本
│   └── start_docker_debug.sh  # 启动 debug 容器脚本
├── tests  # 单元测试
├── .env.template  # .env 文件模板
├── .flaskenv  # flask 环境变量
├── babel.cfg  # 本地化配置
├── boot.sh  # 部署 Docker 启动脚本
├── config.py  # flask 配置读取脚本
├── main.py  # flask 主程序
├── README.md  # README
├── release.dockerfile  # 部署 Docker 镜像构建
├── requirements.txt  # 项目依赖
└── setup.cfg  # 单元测试配置
```

## 3. conda 调试

### 3.1. 安装 pip 依赖

```bash
conda create -n flask_quickstart_venv python=3.6
conda activate flask_quickstart_venv
pip install -r requirements.txt
```

### 3.2. 创建数据库

```sql
-- 创建数据库 flask_quickstart
drop database if exists flask_quickstart;
create database flask_quickstart character set 'utf8' collate 'utf8_general_ci';
-- 创建用户 flask_quickstart 并授权
drop user 'flask_quickstart'@'%';
create user 'flask_quickstart'@'%' identified by 'MySQL@flask_quickstart123456';
flush privileges;
grant all privileges on flask_quickstart.* to 'flask_quickstart'@'%';
flush privileges;
-- 开发环境下还需要创建测试数据库 flask_quickstart_test
drop database if exists flask_quickstart_test;
create database flask_quickstart_test character set 'utf8' collate 'utf8_general_ci';
grant all privileges on flask_quickstart_test.* to 'flask_quickstart'@'%';
flush privileges;
-- 查询 MySQL 的所有用户
select host, user, authentication_string from mysql.user;
-- 查看用户 flask_quickstart 的权限
show grants for 'flask_quickstart'@'%';
```

### 3.3. 修改配置文件

```bash
cp .env.template .env
```

```properties
# .env
APP_NAME=flask_quickstart
SECRET_KEY=a_random_and_long_string
DB_SERVER=localhost
DB_PORT=33060
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

### 3.4. 执行表结构迁移

```bash
# flask db init
# flask db migrate -m "create tables"
flask db upgrade
```

### 3.5. 编译翻译文本

```bash
# flask translate init zh
# flask translate update
flask translate compile
```

### 3.6. 启动调试

```bash
flask run
# or
flask run -h 0.0.0.0 -p 8000
```

```bash
flask shell
```

```bash
flask routes
```

```bash
bash scripts/clean_pycache.sh
```

## 4. Docker 调试

### 4.1. 启动 mysql 容器

```bash
docker pull mysql:8.0
# or
docker pull registry_url/mysql:8.0
```

```bash
docker tag image_id mysql:8.0
```

```bash
# 修改 mysql 数据挂载目录
vim mysql/docker-compose.yml
```

```bash
cd mysql
docker-compose up -d
```

```bash
docker logs -f flask_quickstart_mysql
```

### 4.2. 构建运行时镜像

```bash
cd docker
docker build --squash -t flask_quickstart:latest .
# or
docker pull registry_url/flask_quickstart:latest
```

```bash
docker tag image_id flask_quickstart:latest
```

### 4.3. 启动 debug 容器

```bash
bash script/start_docker_debug.sh
```

```bash
docker exec -it flask_quickstart_debug bash
cd /exec
```

### 4.4. [修改配置文件](#33-修改配置文件)

> 只有调试时需要 `.env` 文件，部署时通过环境变量配置。

### 4.5. [执行表结构迁移](#34-执行表结构迁移)

### 4.6. [编译翻译文本](#35-编译翻译文本)

### 4.7. [启动调试](#36-启动调试)

## 5. Docker 部署

### 5.1. [启动 mysql 容器](#41-启动-mysql-容器)

### 5.2. [构建运行时镜像](#42-构建运行时镜像)

### 5.3. 修改配置文件

```bash
vim config/nginx.conf
```

```bash
vim config/supervisor.conf
```

### 5.4. 构建部署镜像

```bash
docker build --squash -t flask_quickstart:deploy_date -f release.dockerfile .
```

### 5.5. 启动 app 容器

```bash
# 修改 nginx、supervisor、log、tmp 挂载目录
vim config/docker-compose.yml
```

```bash
cd config
docker-compose up -d
```

```bash
docker logs -f flask_quickstart_app
```

```bash
docker exec -it flask_quickstart_app bash
```

```bash
htop
```

```bash
service supervisor status
service nginx status
```

```bash
netstat -tnl | grep 8000
netstat -tnl | grep 8080
```
