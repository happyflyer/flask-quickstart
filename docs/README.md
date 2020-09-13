# 开发者文档

- [apt 使用](apt.md)
- [conda 使用](conda.md)
- [Docker 使用](docker.md)
- [Flask 使用](flask.md)
- [git 使用](git.md)
- [邮箱配置](mail.md)
- [MySQL 使用](mysql.md)
- [Oh My Zsh 使用](oh-my-zsh.md)
- [pip 使用](pip.md)
- [项目测试](test.md)
- [tmux 使用](tmux.md)
- [Ubuntu 使用](ubuntu.md)
- [VSCode 使用](vscode.md)

## 1. clone 代码

```bash
git clone git@gitlab.com:happyflyer/flask-quickstart.git
```

## 2. conda 环境

```bash
conda create -n flaskqs python=3.6.8
conda activate flaskqs
pip install -r docs/requirements.txt
```

## 3. mysql 数据库

```sql
-- 创建数据库
drop database if exists flaskqs;
create database flaskqs character set 'utf8' collate 'utf8_general_ci';
-- 创建测试数据库
drop database if exists flaskqs_test;
create database flaskqs_test character set 'utf8' collate 'utf8_general_ci';
-- 创建用户
drop user 'www' @'%';
create user 'www' @'%' identified by 'password';
flush privileges;
-- 授权
grant all privileges on flaskqs.* to 'www' @'%';
grant all privileges on flaskqs_test.* to 'www' @'%';
flush privileges;
```

```sql
-- 查询用户
select host, user, authentication_string from mysql.user;
-- 查询授权
show grants for 'www' @'%';
```

## 4. 配置文件

```bash
cp .env.template .env
```

```properties
SECRET_KEY=a_random_and_long_string
DB_SERVER=localhost
DB_PORT=3306
DB_USERNAME=www
DB_PASSWORD=password
DB_DATABASE=flaskqs
DB_DATABASE_TEST=flaskqs_test
MAIL_SERVER=
MAIL_PORT=
MAIL_USE_SSL=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_ADMINS=
```

- 执行 `python -c "import uuid; print(uuid.uuid4().hex)"` ，粘贴到 `SECRET_KEY`
- `172.17.0.1` 为 docker 网桥中宿主机默认 ip，其他 `DB` 信息根据需要修改
- `MAIL` 信息配置可参见 [邮箱配置](mail.md)

```properties
# .flaskenv
FLASK_APP=main.py
FLASK_ENV=development
```

## 5. 开发调试

```bash
flask run
```

```bash
flask shell
```

## 6. 打包镜像

```bash
# 构建镜像
docker build -t flask_quickstart_image:latest .
```

```bash
# 导出镜像
docker save image_id > flask_quickstart_docker.tar
```
