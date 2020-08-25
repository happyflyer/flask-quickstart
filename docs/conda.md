# conda 使用

## 1. 虚拟环境管理

```bash
# 创建
conda create -n my_venv python=3.6
conda create -n my_venv python=3.6 numpy
```

```bash
# 所有虚拟环境
conda env list
```

```bash
# *nix 环境下激活
conda activate my_venv
conda deactivate my_venv
```

```powershell
# win 环境下激活
activate my_venv
deactivate my_venv
```

```bash
# 删除
conda remove -n my_venv --all
```

```bash
# 重命名
conda create -n hhh --clone my_venv
conda remove -n my_venv --all
```

## 2. 包管理

```bash
conda list
```

```bash
conda install package_name
```

## 3. 镜像源和代理

```bash
vim ~/.condarc
```

```yaml
channels:
  - defaults
channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
# Show channel URLs when displaying what is going to be downloaded and
# in 'conda list'. The default is False.
show_channel_urls: True
allow_other_channels: True
ssl_verify: False

proxy_servers:
  http: http://代理服务器IP:端口
  https: http://代理服务器IP:端口
```

[anaconda | 镜像站使用帮助 | 清华大学开源软件镜像站 | Tsinghua Open Source Mirror](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)
