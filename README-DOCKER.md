# GPU 容器监控系统 - Docker 版本

## 两种部署方式

### 方式一：守护进程（systemd）
```bash
# 启动服务
sudo systemctl start gpu-monitor

# 停止服务
sudo systemctl stop gpu-monitor

# 查看状态
sudo systemctl status gpu-monitor

# 访问地址
http://10.68.2.212:5000
```

### 方式二：Docker 容器
```bash
# 启动
./start-docker.sh

# 或手动启动
docker-compose up -d

# 停止
docker-compose down

# 查看日志
docker-compose logs -f

# 访问地址
http://10.68.2.212:5001
```

## Docker 版本特点

- ✅ 容器化部署，隔离环境
- ✅ 挂载 Docker socket 监控主机容器
- ✅ 挂载 nvidia-smi 访问 GPU 信息
- ✅ 自动重启（unless-stopped）
- ✅ 使用 host 网络模式
- ✅ 端口 5001（避免与守护进程冲突）

## 端口说明

- 守护进程版本：5000
- Docker 版本：5001

两个版本可以同时运行！

## 依赖

- Docker
- Docker Compose
- NVIDIA Driver
- nvidia-smi

## 文件说明

- `app.py` - 主程序
- `templates/index.html` - Web UI
- `Dockerfile` - Docker 镜像定义
- `docker-compose.yml` - Docker Compose 配置
- `start-docker.sh` - 快速启动脚本
