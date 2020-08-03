# Docker 常用操作

## 1. 容器使用

```bash
docker run -it image_name:image_tag /bin/bash
docker run -it image_id /bin/bash
docker run -itd --name container_name image_id /bin/bash
```

```bash
# ^ = Ctrl
^p + ^q
```

```bash
docker ps
docker ps -a
```

```bash
docker start container_id
docker stop container_id
docker restart container_id
docker attach container_id
```

```bash
# 推荐
docker exec -it container_id /bin/bash
```

```bash
# 导出
docker export container_id > ubuntu.tar
```

```bash
# 导入
cat ubuntu.tar | docker import - my/ubuntu:v1
```

```bash
# 删除一个
docker rm -f container_id
# 删除所有
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
docker search httpd
```

```bash
docker pull ubuntu
docker pull ubuntu:16.04
```

```bash
docker rmi ubuntu:16.04
```

```bash
docker commit -m="message" -a="author" container_id docker/ubuntu:v2
```

```bash
vim Dockerfile
docker build -t docker/ubuntu:v3 .
```

## 4. Dockerfile

每条指令都会生成一个镜像层，Docker 中镜像 **最多 127 层** ，如果超出 Docker Daemon 就会报错。

### 4.1. FROM

设置镜像使用的基础镜像。如果忽略 `tag` 选项，会使用 `latest` 镜像。

```dockerfile
FROM <image>[:<tag>]
```

### 4.2. RUN

编译镜像时运行的脚本。`RUN` 指令会生成容器，在容器中执行脚本，容器使用当前镜像，脚本指令完成后，Docker Daemon 会将该容器提交为一个中间镜像，供后面的指令使用。Dockerfile 的指令每执行一次都会在 docker 上新建一层，过多无意义的层会造成镜像膨胀过大，推荐使用 `&&` 符号连接命令，这样执行后，只会创建 1 层镜像。

```dockerfile
RUN <command>
RUN ["<executable>", "<param1>", "<param2>", ...]
```

```dockerfile
FROM ubuntu
RUN apt-get install wget
RUN wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz"
RUN tar -xvf redis.tar.gz
```

```dockerfile
FROM ubuntu
RUN apt-get install wget && \
    wget -O redis.tar.gz "http://download.redis.io/releases/redis-5.0.3.tar.gz" && \
    tar -xvf redis.tar.gz
```

### 4.3. CMD

设置容器的启动命令。为启动的容器指定默认要运行的程序，程序运行结束，容器也就结束。`CMD` 指令指定的程序可被 `docker run` 命令行参数中指定要运行的程序所覆盖。Dockerfile 中只能有一条 `CMD` 命令，如果写了多条则**最后一条生效**。类似于 `RUN` 指令，用于运行程序，但二者运行的时间点不同:

- `RUN` 在 `docker build` 时执行
- `CMD` 在 `docker run` 时运行

```dockerfile
CMD <command>
CMD ["<executable>", "<param1>", "<param2>", ...]
# 该写法是为 ENTRYPOINT 指令指定的程序提供默认参数
CMD ["<param1>", "<param2>", ...]
```

### 4.4. ENTRYPOINT

设置容器的入口程序。如果运行 `docker run` 时使用了 `--entrypoint` 选项，此选项的参数可当作要运行的程序覆盖 `ENTRYPOINT` 指令指定的程序。类似于 `CMD` 指令，但其不会被 `docker run` 的命令行参数指定的指令所覆盖，而且这些命令行参数会被当作参数送给 `ENTRYPOINT` 指令指定的程序。如果 Dockerfile 中如果存在多个 `ENTRYPOINT` 指令，**仅最后一个生效**。

```dockerfile
ENTRYPOINT ["<executable>", "<param1>", "<param2>", ...]
```

可以搭配 `CMD` 命令使用：一般是变参才会使用 `CMD` ，这里的 `CMD` 等于是在给 `ENTRYPOINT` 传参。

```dockerfile
FROM nginx

ENTRYPOINT ["nginx", "-c"] # 定参
CMD ["/etc/nginx/nginx.conf"] # 变参
```

#### 4.4.1. 不传参运行

```bash
docker run nginx:test
```

容器内会默认运行以下命令，启动主进程。

```bash
nginx -c /etc/nginx/nginx.conf
```

#### 4.4.2. 传参运行

```bash
docker run  nginx:test -c /etc/nginx/new.conf
```

容器内会默认运行以下命令，启动主进程(`/etc/nginx/new.conf`：假设容器内已有此文件)

```bash
nginx -c /etc/nginx/new.conf
```

### 4.5. COPY

复制指令，从上下文目录中复制文件或者目录到容器里指定路径。`<dest>` 为容器内的指定路径，该路径不用事先建好，路径不存在的话，会自动创建。

```dockerfile
COPY [--chown=<user>:<group>] <source1>>... <dest>
COPY [--chown=<user>:<group>] ["<source1>",... "<dest>"]
```

### 4.6. ADD

`ADD` 指令和 `COPY` 的使用格式一致（同样需求下，官方推荐使用 `COPY`）。在执行 `<source>` 为 `tar` 压缩文件的话，压缩格式为 `gzip`, `bzip2` 以及 `xz` 的情况下，会**自动复制并解压**到 `<dest>`。

### 4.7. ENV

设置容器的环境变量。后续的指令中可以通过 `$key` 或 `${key}` 引用。

```dockerfile
ENV <key> <value>
ENV <key1>=<value1> <key2>=<value2> ...
```

### 4.8. ARG

设置编译镜像时加入的参数。与 `ENV` 作用一致。不过作用域不一样。`ARG` 设置的环境变量仅对 Dockerfile 内有效，也就是说只有 `docker build` 的过程中有效，构建好的镜像内不存在此环境变量。

```dockerfile
ARG <key>[=<value>]
```

### 4.9. VOLUME

定义匿名数据卷。在启动容器时忘记挂载数据卷，会自动挂载到匿名卷。在启动容器 `docker run` 的时候，我们可以通过 `-v` 参数修改挂载点。

- 避免重要的数据，因容器重启而丢失，这是非常致命的
- 避免容器不断变大

```dockerfile
VOLUME <path>
VOLUME ["<path1>", "<path2>", ...]
```

### 4.10. EXPOSE

声明镜像要暴露端口。记录容器启动时监听哪些端口。镜像暴露端口可以通过 `docker inspect` 查看。容器启动时，Docker Daemon 会扫描镜像中暴露的端口，如果加入 `-P` 参数，Docker Daemon 会把镜像中所有暴露端口导出，并为每个暴露端口分配一个随机的主机端口（暴露端口是容器监听端口，主机端口为外部访问容器的端口）。`EXPOSE` 只声明暴露端口并不导出端口，只有启动容器时使用 `-P`/`-p` 才导出端口，这个时候才能通过外部访问容器提供的服务。

```dockerfile
EXPOSE <port1> [<port2> ...]
```

### 4.11. WORKDIR

指定 `RUN` `CMD` `ENTRYPOINT` `COPY` `ADD` 指令的工作目录。用 `WORKDIR` 指定的工作目录，会在构建镜像的每一层中都存在。

```dockerfile
WORKDIR <path>
```

### 4.12. USER

设置运行 `RUN` `CMD` `ENTRYPOINT` 指令的用户。

```dockerfile
USER <username>[:<group>]
```

[Docker 教程菜鸟教程](https://www.runoob.com/docker/docker-hello-world.html)
