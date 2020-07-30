# 项目测试

## 1. 测试准备

- 测试代码位于 `tests` 文件夹中
- 单元测试模块都以 `test_` 开头
- 测试函数都以 `test_` 开头
- 测试配置文件为 `setup.cfg`

## 2. 运行测试

```bash
pytest
```

```bash
pytest -v
```

## 3. 测试覆盖

```bash
coverage run -m pytest
```

```bash
coverage report
```
