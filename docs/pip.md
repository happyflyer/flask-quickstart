# pip 使用

## 1. 包管理

```bash
pip install -r requirements.txt
```

```bash
pip freeze > requirements.txt
```

## 2. 镜像源和代理

```bash
vim ~/.config/pip/pip.conf
```

```properties
[global]
disable-pip-version-check = True
proxy = http://代理服务器IP:端口
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```

## 3. zeroc-ice 安装时的依赖

```bash
sudo apt-get install -y libssl-dev
sudo apt-get install -y libboost-all-dev
sudo apt-get install -y libbz2-dev
```
