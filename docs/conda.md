# conda 常用操作和配置

## 1. 虚拟环境

```bash
conda create -n my_venv python=3.6
conda create -n my_venv python=3.6 numpy
```

```bash
conda env list
```

```bash
conda activate my_venv
conda deactivate my_venv
```

```powershell
activate my_venv
deactivate my_venv
```

```bash
conda info
```

```bash
conda remove -n my_venv --all
```

```bash
# 重命名
conda create -n hhh --clone my_venv
conda remove -n my_venv --all
```

## 2. 镜像源和代理

```bash
vim ~/.condarc
```

```properties
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

proxy_servers:
  http: http://代理服务器IP:端口
  https: http://代理服务器IP:端口

ssl_verify: False
```

[Anaconda 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)
