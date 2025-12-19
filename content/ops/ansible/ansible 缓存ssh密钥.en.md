---
categories:
- Operations Maintenance
date: 2024-11-26 02:00:00
draft: false
tags:
- Ansible
title: ansible | Cache SSH key to avoid password input each time
---

# Background
When using Ansible, to avoid the need to enter the SSH password each time a task is executed, we can cache the SSH key.

# Caching SSH Keys with Ansible

1. Start the ssh-agent background program

eval "$(ssh-agent -s)"

2. Add the key to ssh-add, only input the password once

ssh-add ~/.ssh/xxx

3. Verify if the key is successfully cached

ssh-add -l