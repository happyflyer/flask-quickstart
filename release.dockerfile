# 使用方法：docker build --squash -t <NAME>:<TAG> -f release.dockerfile .

FROM flask_quickstart:latest

# 工作路径是可执行文件存放路径
WORKDIR /exec

# 发布后默认启动boot.sh，项目根目录在启动时默认挂载在/project
CMD ["bash", "/exec/boot.sh"]

# 复制本目录所有文件
COPY . .

# 编译可执行文件，删除无用的文件
RUN rm -rf .git docker mysql scripts tests && \
    rm -f .env.template .gitattributes .gitignore README.md requirements.txt \
    release.dockerfile config/docker-compose.yml
