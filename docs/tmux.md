# tmux 常用操作

`prefix` 默认为： `Ctrl` + `b`

## 1. session

```bash
tmux new -s s1
```

```bash
tmux ls
```

```bash
prefix d
```

```bash
tmux a -t s1
tmux a
```

```bash
tmux rename -t s1 s2
```

```bash
tmux kill-session
tmux kill-session -t s1
# 关闭除s1外的其他
tmux kill-session -a -t s1
# 关闭所有
tmux kill-server
```

```bash
# 列出所有session，切换
prefix s
```

```bash
# 为当前session命名
prefix $
```

## 2. window

```bash
prefix c
```

```bash
prefix <n>
```

```bash
prefix ,
```

```bash
# 列出所有window，切换
prefix w
```

```bash
# 关闭当前window
prefix &
```

## 3. panel

```bash
# 垂直切分pane，分为左和右
prefix %
# 水平切分pane，分为上和下
prefix "
```

```bash
# 切换panel布局
prefix <space>
```

```bash
# 顺时针切换pane
prefix o
```

```bash
# 与下一个窗格交换位置
prefix }
# 与上一个窗格交换位置
prefix {
```

```bash
# 显示窗格编号
prefix q
```

```bash
# 显示一个时钟
prefix t
```

## 4. help

```bash
# 显示快捷键帮助列表，按q退出
prefix ?
```

[tmux 基本操作](https://www.cnblogs.com/liuguanglin/p/9290345.html)

[优雅地使用命令行：Tmux 终端复用](https://harttle.land/2015/11/06/tmux-startup.html)
