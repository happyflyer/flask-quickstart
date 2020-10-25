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

## 1. 创建 conda 环境

```bash
conda create -n flask_quickstart_venv python=3.6.8
conda activate flask_quickstart_venv
pip install -r docs/requirements.txt
```

## 2. 创建数据库

[create_database_and_user.sql](../scripts/create_database_and_user.sql)

## 3. 创建配置文件

```bash
cp .env.template .env
```

```properties
# .flaskenv
FLASK_APP=main.py
FLASK_ENV=development
```
