---
title: "Hugo ｜ 本地服务器部署"
date: 2025-12-07T18:31:24+08:00
draft: false
categories:
    - 博客
---

以前采用的是github pages部署网站，现在进行服务器部署网站。

## 安装基础软件
```bash
#  更新系统并安装 EPEL 源
sudo yum update -y
sudo yum install epel-release -y

# 安装 Nginx, Git, 和 Certbot
sudo yum install nginx git certbot certbot-nginx -y

# 启动 Nginx 并设置开机自启
sudo systemctl start nginx
sudo systemctl enable nginx

# 创建目录
sudo mkdir -p /var/www/hangops

sudo chown -R root:root /var/www/hangops
sudo chmod -R 755 /var/www/hangops
```
## 配置 Nginx 与 HTTPS
```bash
sudo vi /etc/nginx/conf.d/hangops.top.conf

# 检查语法是否正确
sudo nginx -t 
# 如果显示 successful，则重启
sudo systemctl reload nginx
```

nginx 配置

```bash
server {
    listen 80;
    server_name hangops.top www.hangops.top;

    root /var/www/hangops;
    index index.html;

    # 核心：处理 Hugo 的路由（防止刷新 404）
    location / {
        try_files $uri $uri/ =404;
    }

    # SRE 优化：开启 Gzip 压缩，加速访问
    gzip on;
    gzip_min_length 1k;
    gzip_comp_level 5;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

### 申请 HTTPS 证书
sudo certbot --nginx -d hangops.top -d www.hangops.top


## 配置 GitHub 自动部署 (CI/CD)
看仓库源码即可

