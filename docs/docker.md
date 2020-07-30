# Docker 常用操作

## 1. 容器使用

```bash
docker run -it ubuntu /bin/bash
docker run -itd --name ubuntu-test ubuntu /bin/bash
```

```bash
^p + ^q
exit
```

```bash
docker ps
docker ps -a
```

```bash
docker start container_id
docker stop container_id
docker restart container_id
```

```bash
docker attach container_id
```

```bash
docker exec -it container_id /bin/bash
```

```bash
docker export container_id > ubuntu.tar
```

```bash
cat ubuntu.tar | docker import - test/ubuntu:v1
```

```bash
docker rm -f container_id
docker container prune
```

## 2. Web 容器使用

```bash
docker pull training/webapp
docker run -d -P training/webapp python app.py
docker run -d -p 5000:5000 training/webapp python app.py
```

```bash
docker port container_id
```

```bash
docker logs -f container_id
```

```bash
docker top container_id
```

## 3. 镜像使用

```bash
docker images
```

```bash
docker pull ubuntu
docker pull ubuntu:16.04
```

```bash
docker search httpd
```

```bash
docker run -it ubuntu:16.04 /bin/bash
```

```bash
docker rmi hello-world
```

```bash
docker commit -m="message" -a="author" <image-id> docker/ubuntu:v2
```

```bash
vim Dockerfile
docker build -t docker/ubuntu:tag .
```

## 4. Dockerfile

```dockerfile
FROM nginx
RUN echo '这是一个本地构建的nginx镜像' > /usr/share/nginx/html/index.html
```

```dockerfile
RUN <命令行命令>
# <命令行命令> 等同于，在终端操作的 shell 命令。
RUN ["可执行文件", "参数1", "参数2"]
```

[Docker 教程菜鸟教程](https://www.runoob.com/docker/docker-hello-world.html)
