# Oh My Zsh 安装和插件

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
# 码云
sh -c "$(curl -fsSL https://gitee.com/shmhlsy/oh-my-zsh-install.sh/raw/master/install.sh)"
```

## 3. autojump

```bash
sudo apt-get install autojump
```

```bash
vim ~/.zshrc
# . /usr/share/autojump/autojump.sh
```

## 4. zsh-syntax-highlighting

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git
```

```bash
vim ~/.zshrc
# source ${(q-)PWD}/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
```

## 5. zsh-autosuggestions

```bash
git clone git://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
```

```bash
vim ~/.zshrc
# plugins=(
#     git
#     zsh-autosuggestions
# )
# source $ZSH_CUSTOM/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
```
