# Flask 命令操作

## 1. 开发调试

```bash
# 开发调试，默认绑定端口：http://127.0.0.1:5000/
flask run
```

```bash
# 交互界面调式
flask shell
```

```bash
# 查看路由规则
flask routes
```

## 2. 数据库迁移

```bash
# 初始化
flask db init
```

```bash
# 迁移
flask db migrate -m "create table"
```

```bash
# 升级
flask db upgrade
# 降级
flask db downgrade
```

## 3. 本地化

```bash
# 抽取翻译文本，执行之前检查 babel.cfg 文件是否存在
pybabel extract -F babel.cfg -k _l -o messages.pot .
# 创建语言 zh
pybabel init -i messages.pot -d app/translations -l zh
# 编译
pybabel compile -d app/translations
# 更新
pybabel extract -F babel.cfg -k _l -o messages.pot .
pybabel update -i messages.pot -d app/translations
```

```bash
# 自定义babel命令(在app/cli.py中定义)
# 初始化 zh
flask translate init zh
# 更新
flask translate update
# 编辑 app/translations/zh/.../message.po
# 编译
flask translate compile
```
