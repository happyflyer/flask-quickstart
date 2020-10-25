# Oh My Zsh 使用

> 安装过程为 ubuntu 版本。

## 1. zsh

```bash
sudo apt-get install zsh
```

## 2. ob my zsh

```bash
# 安装 oh-my-zsh
# sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
sh -c "$(curl -fsSL https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh)"
```

## 3. 插件

```bash
sudo apt-get install autojump git
```

```bash
git clone https://gitee.com/mirror-github/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
git clone https://gitee.com/mirror-github/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
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
