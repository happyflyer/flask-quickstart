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
- `data`：初始化数据，应用程序运行时产生的缓存数据放到 `tmp`
- `docs`：开发者文档
- `migrations`：数据库迁移记录
- `scripts`：数据库初始化脚本
- `tests`：单元测试
- `config.py`：用于加载配置文件
- `main.py`：用于启动应用程序

## 4. 部署

### 4.1. 创建数据库容器

```bash
docker pull mysql:5.7
```

```bash
docker run -itd \
  --name flask_quickstart_mysql \
  --restart=always \
  -p 23001:3306 \
  -v $(pwd)/scripts:/docker-entrypoint-initdb.d \
  -e MYSQL_ROOT_PASSWORD=root_password \
  mysql:5.7
```

### 4.2. 创建配置文件

```bash
cp .env.template .env
```

- 执行 `python -c "import uuid; print(uuid.uuid4().hex)"` ，粘贴到 `SECRET_KEY`
- `172.17.0.1` 为 docker 网桥中宿主机默认 ip
- `MAIL` 信息配置可参见 [邮箱配置](docs/mail.md)

### 4.3. 启动应用程序容器

```bash
chmod +x boot.sh
docker run -itd \
  --name=flask_quickstart_container \
  -p 8080:8080 \
  --restart=always \
  -v $(pwd):/DATACENTER1/flask-quickstart \
  flask_quickstart:latest /DATACENTER1/flask-quickstart/boot.sh
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
