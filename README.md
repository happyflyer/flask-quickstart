# Flask Quickstart

## 1. 介绍

Flask Quickstart 是一个具有 Web 后端基本功能、易于快读二次开发的 Flask 项目。

## 2. 特点

- 界面和接口，所有功能接口化
- 权限控制，用户、模块、权限三维控制
- 访问统计，记录所有非匿名访问请求
- 运维日志，文件日志和错误邮件
- 语言本地化，集成babel
- 单元测试，得到测试覆盖率报告
- 接口文档，文档和代码合于一处，项目启动后访问 `/docs/api`
- [开发文档](docs/README.md)，各类文档丰富

## 3. 部署

### 3.1. 启动前准备

```bash
# 安装依赖
pip install -r requirements.txt
```

```bash
# 生成密钥，并配置到 .env
cp .env.template .env
python -c "import uuid; print(uuid.uuid4().hex)"
```

```bash
# .env 设置好数据库连接信息字段
# 执行 script/create_database_and_user.sql 操作创建数据库、创建用户、对用户授权
# 执行数据库升级
flask db upgrade
```

```bash
# 文本资源编译，会在 app/translation 文件夹下生成 *.mo 文件
flask translate compile
```

### 3.2. 托管启动

```bash
sudo cp supervisor.conf /etc/supervisor/conf.d/flask_quickstart.conf
sudo supervisorctl reload
```

```bash
sudo rm /etc/nginx/sites-enabled/default
# sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
```

```bash
sudo cp nginx.conf /etc/nginx/sites-enabled/
sudo service nginx reload
```

### 3.3. 升级更新

```bash
git pull
```

```bash
sudo supervisorctl stop flask_quickstart
```

```bash
flask db upgrade
flask translate compile
```

```bash
sudo supervisorctl start flask_quickstart
```
