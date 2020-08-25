# 邮箱配置

## 1. qq 邮箱设置

> 设置 > 账户 > POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务

```properties
MAIL_SERVER=smtp.qq.com
MAIL_PORT=<465或者587>
MAIL_USE_SSL=1
MAIL_USERNAME=<qq账号>
MAIL_PASSWORD=<qq邮箱授权码>
MAIL_ADMINS=<邮箱，多个邮箱之间用','分隔>
```

## 2. 163 邮箱设置

> 设置 > POP3/SMTP/IMAP > 授权密码管理

```properties
MAIL_SERVER=smtp.163.com
MAIL_USE_SSL=1
MAIL_USERNAME=<163邮箱>
MAIL_PASSWORD=<163邮箱授权码>
MAIL_ADMINS=<邮箱，多个邮箱之间用','分隔>
```
