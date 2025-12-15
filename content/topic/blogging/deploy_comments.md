---
title: "博客 | 本地部署waline 评论系统"
date: 2025-12-14T17:53:12+08:00
draft: false
categories:
    - "博客"
---
## Waline 评论系统
博客原本使用github giscus 作为评论系统，现在迁移至 Waline 评论系统。
- 支持匿名评论（无需登录）
- UI 简洁美观
- 可以配置邮箱/weixin 接收通知


## 本地部署(Waline)

### docker-compose 部署
```yaml
version: '3'

services:
  waline:
    image: lizheming/waline:latest
    container_name: waline-standalone
    restart: always
    ports:
      - "8360:8360"
    environment:
      - MYSQL_HOST=blog-stats-db  
      - MYSQL_PORT=3306
      - MYSQL_DB=waline_db        
      - MYSQL_USER=root
      - MYSQL_PASSWORD=xxx
      - MYSQL_CHARSET=utf8mb4
      - MYSQL_SSL=false
      - TABLE_PREFIX=wl_

      - TZ=Asia/Shanghai
      - LANG=zh_CN.UTF-8
      - JWT_SECRET=Standalone_Waline_Secret_2025

      # --- 通知配置 ---
      - SITE_NAME=Hangliuc
      - SITE_URL=https://hangops.top

      # 163
      - SMTP_SERVICE=163
      - SMTP_USER=iliuhang@163.com
      - SMTP_PASS=xxxxx
      - SMTP_SECURE=true
      - AUTHOR_EMAIL=iliuhang@163.com
      - SENDER_EMAIL=iliuhang@163.com

    networks:
      - ext-blog-net

networks:
  ext-blog-net:
    external: true
    name: blog-stats_blog-net   #因为 Waline 和 MySQL 不在同一个 docker-compose.yaml 文件里，它们默认是隔离的。需要让 Waline 加入到 MySQL 所在的网络中。


```
使用时请先导入 waline.sql 以完成表和表结构的创建，之后在项目中配置如下环境变量。
[Waline 数据库配置](https://waline.js.org/guide/database.html#mysql)

```shell
docker exec -i blog-stats-db   mysql -uroot -p'xxxxx' -Dwaline_db < waline.sql
```

### Nginx 反向代理
```nginx
server {
    if ($host = comment.hangops.top) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name comment.hangops.top;

    # 强制跳转 HTTPS (可选，建议加上)
    return 301 https://$host$request_uri;


}

server {
    listen 443 ssl http2;
    server_name comment.hangops.top;

    ssl_certificate /etc/letsencrypt/live/comment.hangops.top/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/comment.hangops.top/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8360;

        # 必须带上的 Header，否则 Waline 无法获取用户真实
	proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    ssl_certificate /etc/letsencrypt/live/comment.hangops.top/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/comment.hangops.top/privkey.pem; # managed by Certbot
}
```

### Hugo 配置

[Waline 组件配置](https://waline.js.org/reference/client/props.html)
```yaml
params:
    comments:
        enabled: true
        provider: waline
        waline:
            serverURL: https://comment.hangops.top
            pageview: true # 开启阅读量
            requiredMeta:
                - nick
                - mail 
```

