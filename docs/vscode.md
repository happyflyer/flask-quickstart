# VSCode 设置

## 1. sftp 插件

```json
{
  "name": "name",
  "host": "ip",
  "protocol": "sftp",
  "port": 22,
  "username": "username",
  "password": "password",
  "remotePath": "path",
  "uploadOnSave": true,
  "ignore": [
    ".vscode",
    ".git",
    ".DS_Store",
    "**/__pycache__",
    "venv",
    "log",
    "tmp",
    "**/*.db",
    "**/*.mo"
  ],
  "watcher": {
    "files": "**/*",
    "autoUpload": true,
    "autoDelete": true
  }
}
```

## 2. python 插件

```json
"python.formatting.autopep8Args": [
    "--max-line-length=112",
]
```
