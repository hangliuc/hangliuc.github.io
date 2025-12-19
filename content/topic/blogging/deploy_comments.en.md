---
categories:
- Blog
date: 2025-12-14 09:53:12
draft: false
title: Hugo | Waline comment system private deployment
---

## Waline Comment System
The blog originally used GitHub Giscus as the comment system, but has now migrated to the Waline comment system.
- Supports anonymous comments (no login required)
- Simple and beautiful UI
- Can be configured to receive notifications via email/weixin

## Local Deployment (Waline)

### Docker Compose Deployment
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

      # --- Notification Configuration ---
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
    name: blog-stats_blog-net   # Because Waline and MySQL are not in the same docker-compose.yaml file, they are isolated by default. Waline needs to be added to the network where MySQL is located.
```
When using, please import `waline.sql` first to complete the creation of tables and table structures, and then configure the following environment variables in the project.
[Waline Database Configuration](https://waline.js.org/guide/database.html#mysql)

```shell
docker exec -i blog-stats-db   mysql -uroot -p'xxxxx' -Dwaline_db < waline.sql
```

### Nginx Reverse Proxy
```nginx
server {
    if ($host = comment.hangops.top) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name comment.hangops.top;

    # Force redirection to HTTPS (optional, recommended to add)
    return 301 https://$host$request_uri;


}

server {
    listen 443 ssl http2;
    server_name comment.hangops.top;

    ssl_certificate /etc/letsencrypt/live/comment.hangops.top/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/comment.hangops.top/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8360;

        # Headers that must be included, otherwise Waline cannot obtain the real user
	proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    ssl_certificate /etc/letsencrypt/live/comment.hangops.top/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/comment.hangops.top/privkey.pem; # managed by Certbot
}
```

### Hugo Configuration

[Waline Component Configuration](https://waline.js.org/reference/client/props.html)
```yaml
params:
    comments:
        enabled: true
        provider: waline
        waline:
            serverURL: https://comment.hangops.top
            pageview: true # Enable page views
            requiredMeta:
                - nick
                - mail 
```