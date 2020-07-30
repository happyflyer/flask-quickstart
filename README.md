# Flask Quickstart

## 1. 介绍

Flask Quickstart 是一个具有 Web 后端基本功能、易于快读二次开发的 Flask 项目。

## 2. 特点

- 界面和接口
- 权限控制
- 访问统计
- 运维日志
- 语言本地化
- 单元测试
- 接口文档
- [开发文档](docs/README.md)

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
# .env 设置好数据库连接信息字段后，执行数据库升级
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
