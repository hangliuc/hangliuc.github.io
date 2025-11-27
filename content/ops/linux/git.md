---
title: "Git"
date: 2025-11-27T11:01:37+08:00
draft: false
categories:
    - 运维
tags:
    - command
---
# git 命令使用


#### 基本命令

```
1. 初始化仓库
命令： git init
2. 克隆远程仓库
命令： git clone <repository_url>
3. 查看当前仓库状态
命令： git status
4. 查看提交日志
命令： git log
5. 添加文件到暂存区
命令： git add <file_name>
6. 提交更改
命令： git commit -m "message"
7. 查看仓库的配置信息
命令： git config --list
```

#### 分支操作

```
1.查看所有分支：
git branch
2.创建新分支：
git branch <branch_name>
3.切换分支：
git checkout <branch_name>：
4.创建并切换到新分支：
git checkout -b <branch_name>
5.删除分支：
git branch -d <branch_name>
6.查看当前分支：
git branch --show-current
```

#### 合并分支

```
1. 合并分支
命令： git merge <branch_name>
```

#### 远程操作

```
1.查看远程仓库信息：
命令： git remote -v
2.添加远程仓库：
git remote add origin <repository_url>
3.推送更改到远程仓库：
命令： git push origin <branch_name>
4.拉取远程仓库的更改：
命令： git pull origin <branch_name>
5.获取远程仓库的最新更改（不合并）：
命令： git fetch origin
```

#### 文件操作

```
1. 查看文件历史
命令： git log <file_name>
2. 撤销对文件的修改（还原到暂存区状态）
命令： git checkout -- <file_name>
3. 恢复文件到最后一次提交的状态
命令： git restore <file_name>
4. 删除文件并提交
命令：git rm <file_name>：从暂存区和工作区删除文件。
```

#### 其他常用操作

```
1. 显示差异
命令： git diff
作用： 显示工作目录与暂存区之间的差异，或者已暂存的文件与上次提交之间的差异。
示例：
git diff: 显示工作区与暂存区的所有差异。
git diff --cached: 显示暂存区与上次提交的差异。
2. 撤销提交（回到上一个提交）
命令： git reset --hard HEAD~1
作用： 将HEAD指针移动到上一个提交，并丢弃当前分支上的所有提交。注意： 这个操作是危险的，会丢失未提交的更改。
解释：
HEAD~1: 指向上一个提交。
--hard: 除了移动HEAD指针，还将工作目录和暂存区重置为上一个提交的状态。
3. 暂存文件但不提交
命令： git stash
作用： 将当前工作目录的修改暂存起来，以便稍后恢复。这通常用于在切换分支或执行其他操作前保存当前工作。
示例：
git stash: 暂存所有修改。
git stash save "message": 暂存修改并添加一个描述信息。
恢复暂存的修改：
git stash pop: 恢复最近一次暂存的修改。
git stash list: 查看所有的暂存。
git stash apply: 应用指定的暂存，但不删除它。
```