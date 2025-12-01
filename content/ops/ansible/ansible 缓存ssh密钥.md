---
title: "缓存ssh密钥"
date: 2023-11-26T10:00:00+08:00
draft: false

categories:
    - 运维
    - 
tags:
    - ansible
---
# 背景
使用ansible时，为了避免每次执行任务都需要输入ssh密码，我们可以缓存ssh密钥。

# ansible 缓存ssh密钥

1. 启动 ssh-agent 后台程序

eval "$(ssh-agent -s)"

2. 将密钥添加至 ssh-add，只输入一次密码

ssh-add ~/.ssh/xxx

3. 验证密钥是否缓存成功

ssh-add -l