# Oh My Zsh 使用

> 安装过程为 ubuntu 版本。

## 1. zsh

```bash
sudo apt-get install zsh
```

```bash
# 把默认的 shell 改成 zsh ，不要使用 sudo
chsh -s /bin/zsh
```

## 2. ob my zsh

```bash
sudo apt-get install git
```

```bash
# 安装 oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
# 建议使用 gitee 镜像
sh -c "$(curl -fsSL https://gitee.com/shmhlsy/oh-my-zsh-install.sh/raw/master/install.sh)"
```

## 3. 插件

```bash
sudo apt-get install autojump
```

```bash
# 建议使用 gitee 镜像
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
```

```bash
# 建议使用 gitee 镜像
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
```

```bash
vim ~/.zshrc
```

```properties
plugins=(
    git
    zsh-autosuggestions
)
. /usr/share/autojump/autojump.sh
source $ZSH_CUSTOM/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source $ZSH_CUSTOM/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
```
