# Ubuntu 使用

## 1. 创建用户

使用 **useradd** 命令创建新用户时:

- 不会为用户创建主目录
- 不会为用户指定 shell 版本
- 不会为用户创建密码

```bash
sudo useradd tt
sudo usermod -d /home/tt tt
sudo usermod -s /bin/bash tt
sudo passwd tt
```

```bash
sudo useradd -d /home/tt -m -s /bin/bash tt
sudo passwd tt
```

## 2. 删除用户

```bash
sudo userdel tt
sudo userdel -r tt
```
