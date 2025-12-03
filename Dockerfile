FROM python:3.11-slim

WORKDIR /app

# 安装 Docker CLI
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir flask

# 复制应用文件
COPY app.py /app/
COPY templates /app/templates/

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "app.py"]
