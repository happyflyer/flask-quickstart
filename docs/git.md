# git 使用

## 1. 全局配置

```bash
# 设置用户名
git config --global user.name "your_name"
```

```bash
# 设置邮件
git config --global user.email "your_email@example.com"
```

```bash
# 提交时转换为LF，检出时不转换
git config --global core.autocrlf input
```

```bash
# 拒绝提交包含混合换行符的文件
git config --global core.safecrlf true
```

## 2. 日常使用

```bash
git clone git@github.com:github/gitignore.git
```

```bash
git init
```

```bash
git add doc.txt
git commit -m "add doc.txt"
```

```bash
git status
```

```bash
git diff doc.txt
```

## 3. 日志和切换

```bash
# 提交日志
git log
git log --pretty=oneline
git log --oneline --graph --decorate --all
git reflog
```

```bash
# 回退到指定提交版本
git reset --hard commit_id
```

## 4. 撤销和丢弃

```bash
# 撤销暂存区的修改
git reset HEAD doc.txt
```

```bash
# 丢弃工作区的修改
git checkout -- doc.txt
```

- `doc.txt` 自修改后还没有被放到暂存区，撤销修改就回到**和版本库一模一样的状态**。
- `doc.txt` 已经添加到暂存区后，又作了修改，撤销修改就回到**添加到暂存区后的状态**。

## 5. 删除和恢复

```bash
# 删除工作区和版本库的文件
rm doc.txt
git rm doc.txt
git commit -m "del doc.txt"
```

```bash
# 删除了工作区的文件后，从版本库恢复
rm doc.txt
git checkout -- doc.txt
```

## 分支与标签

```bash
git checkout -b dev
git checkout dev
```

```bash
git tag 0.1.0
git checkout 0.1.0
```

```bash
git checkout master
git merge dev
```

## 6. 关联远程仓库

```bash
ssh-keygen -t rsa -C "your_message"
```

将公钥 ~/.ssh/id_rsa.pub 添加到 github/gitlab/gitee/.. 账户的 SSH 公钥。

```bash
# 测试
ssh -T git@github.com
```

```bash
git remote add origin git@server_name:username/repo_name.git
```

```bash
git remote
git remote -v
```

## 7. 拉取和推送

```bash
# git pull <远程主机名> <远程分支名>:<本地分支名>
git pull origin next:master
# pull = fetch + merge
```

```bash
# git push <远程主机名> <本地分支名>:<远程分支名>
# 首次推送时，加'-u'参数
git push origin master
git push origin --all
git push origin --tags
```

```bash
git tag -d 0.1.0
git push origin :refs/tags/0.1.0
```

[Git 教程 - 廖雪峰的官方网站](https://www.liaoxuefeng.com/wiki/896043488029600)

[git clone，push，pull，fetch 命令详解（转载） - xiaopang1983 - 博客园](https://www.cnblogs.com/xiaopangjr/p/7469687.html)
