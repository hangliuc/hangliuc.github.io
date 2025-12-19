---
categories:
- Blog
date: 2025-12-07 10:31:24
draft: false
title: Hugo | Local Server Deployment
---

## Previous Deployment Method: GitHub Pages
Now, we are deploying the website on a server.

## Installing Basic Software
```bash
# Update the system and install the EPEL repository
sudo yum update -y
sudo yum install epel-release -y

# Install Nginx, Git, and Certbot
sudo yum install nginx git certbot certbot-nginx -y

# Start Nginx and set it to start on boot
sudo systemctl start nginx
sudo systemctl enable nginx

# Create directories
sudo mkdir -p /var/www/hangops

sudo chown -R root:root /var/www/hangops
sudo chmod -R 755 /var/www/hangops
```

## Configuring Nginx and HTTPS
```bash
sudo vi /etc/nginx/conf.d/hangops.top.conf

# Check if the syntax is correct
sudo nginx -t 
# If it shows successful, then restart
sudo systemctl reload nginx
```

nginx configuration

```bash
server {
    listen 80;
    server_name hangops.top www.hangops.top;

    root /var/www/hangops;
    index index.html;

    # Core: Handle Hugo's routing (prevent 404 on refresh)
    location / {
        try_files $uri $uri/ =404;
    }

    # SRE Optimization: Enable Gzip compression to accelerate access
    gzip on;
    gzip_min_length 1k;
    gzip_comp_level 5;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

### Applying HTTPS Certificate
sudo certbot --nginx -d hangops.top -d www.hangops.top

## Configuring GitHub Auto-Deployment (CI/CD)
Check the repository source code for details.