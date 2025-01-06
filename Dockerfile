# 定义镜像的标签
ARG TAG=3.13-slim-bullseye

# 阶段 1: 构建镜像
# 使用官方 Python 镜像
FROM python:${TAG} as base

# pip镜像源
ENV PIPURL "https://mirrors.aliyun.com/pypi/simple/"
# ENV PIPURL "https://pypi.org/simple/"

# 设置工作目录
WORKDIR /app

# 复制项目依赖文件到容器
COPY pdm.lock .

# 安装 pdm 及项目依赖
RUN pip install --no-cache-dir pdm -i ${PIPURL} --default-timeout=1000 \
    && pdm export -o requirements.txt --without-hashes


# 阶段 2: 运行时镜像
FROM python:${TAG}

# 设置工作目录
WORKDIR /app

# 复制构建产物
COPY --from=base /app/requirements.txt /app/requirements.txt

# pip镜像源
ENV PIPURL "https://mirrors.aliyun.com/pypi/simple/"
# ENV PIPURL "https://pypi.org/simple/"

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt -i ${PIPURL} --default-timeout=1000

# 复制应用代码到容器
COPY . /app

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]