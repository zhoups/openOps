

[![Python3](https://img.shields.io/badge/python-3.6-green.svg?style=plastic)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-1.11-brightgreen.svg?style=plastic)](https://www.djangoproject.com/)
[![Ansible](https://img.shields.io/badge/ansible-2.2.2.0-blue.svg?style=plastic)](https://www.ansible.com/)
[![Paramiko](https://img.shields.io/badge/paramiko-2.1.2-green.svg?style=plastic)](http://www.paramiko.org/)

blueops is a open source proxy server, developed by `Python` and `Django`, aim to help
companies to efficiently user, assets, authority and audit management

blueops是一款使用Python, Django开发的开源跳板机系统, 助力互联网企业高效 用户、资产、权限、审计 管理

### Feature 功能
  - Auth 统一认证
  - CMDB 资产管理
  - Perm 统一授权
  - Audit 审计
  - LDAP AUTH 支持LDAP认证
  - Web terminal
  - SSH Server


### Environment 环境
   * Python 3.6  
   * Django 1.11

### 快速启动

```
$ docker run -p 8080:80 -p 2222:2222 blueops/blueops:0.5.0-beta2
```
更多见 [Dockerfile](https://github.com/blueops/Dockerfile.git)

### 详细安装步骤

    1,同步数据库，直接python manage.py migrate,要用原来的数据迁移文件
    2,创建超级管理员
    3,python manage.py runserver 0.0.0.0:8000


### Usage 使用
   1. Visit http://$HOST:8080 (访问 http://你的主机IP:8080 来访问 blueops)
 
   2. Click left navigation visit Applications-Terminal and accept coco and luna register
      (点击左侧 应用程序接受 Coco注册)
   
   3. Click Assets-Admin user, Create admin user
      (添加 管理用户)
   
   4. Click Assets-System user, Create system user
      (添加 系统用户)
      
   5. Click Assets-Asset, Add a asset
      (添加 资产)
   
   6. Click Perms-Asset permission, Add a perm rule
      (添加授权规则，授权给admin)
   
   7. Connect ssh server coco (连接 ssh server coco)
      
      ssh -p2222 $USER@$Host
 

   
### Snapshot 截图

    https://github.com/blueops/blueops/issues/438



