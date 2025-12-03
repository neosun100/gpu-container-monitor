# 🚀 GPU 容器监控系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

> 一个美观的、实时的 GPU 容器监控仪表板，具有全面的管理功能。

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md)

![GPU 容器监控仪表板](https://via.placeholder.com/800x400/667eea/ffffff?text=GPU+Container+Monitor+Dashboard)

## ✨ 功能特性

- 🎮 **实时 GPU 监控** - 监控所有 NVIDIA GPU 的实时指标
  - GPU 利用率和显存使用
  - 温度和功耗
  - 可视化进度条，易于阅读
  
- 📦 **容器管理** - 完全控制使用 GPU 的容器
  - 启动、停止、暂停和重启容器
  - 彩色状态指示器查看容器状态
  - 查看每个容器使用的 GPU
  
- 🎨 **精美界面** - 现代化、响应式 Web 界面
  - 渐变色主题
  - 实时更新（1秒/3秒/5秒/10秒间隔）
  - 状态图例快速参考
  - 移动端友好设计
  
- 🔄 **双重部署选项**
  - Systemd 服务（轻量级）
  - Docker 容器（隔离环境）
  
- 🌐 **多语言支持** - 英语、简体中文、繁体中文、日语

## 📋 前置要求

安装前，请确保您具备以下条件：

### 必需项

- **操作系统**：Linux（Ubuntu 20.04+、Debian 11+ 或类似系统）
- **NVIDIA GPU**：一个或多个 NVIDIA GPU
- **NVIDIA 驱动**：版本 450.80.02 或更高
- **nvidia-smi**：NVIDIA 系统管理接口
- **Docker**：版本 20.10+ 并安装 NVIDIA Container Toolkit
- **Python**：版本 3.8 或更高

### 快速检查

运行此命令验证您的系统：

```bash
# 检查 NVIDIA 驱动和 GPU
nvidia-smi

# 检查 Docker
docker --version

# 检查 Python
python3 --version

# 检查 NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### 安装前置依赖

<details>
<summary><b>Ubuntu/Debian</b></summary>

```bash
# 安装 NVIDIA 驱动（如果未安装）
sudo apt update
sudo apt install nvidia-driver-535

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 安装 Python 和 pip
sudo apt install python3 python3-pip

# 安装 Flask
pip3 install flask
```

</details>

<details>
<summary><b>CentOS/RHEL</b></summary>

```bash
# 安装 NVIDIA 驱动
sudo yum install nvidia-driver

# 安装 Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io

# 安装 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | \
  sudo tee /etc/yum.repos.d/nvidia-docker.repo

sudo yum install -y nvidia-container-toolkit
sudo systemctl restart docker

# 安装 Python 和 pip
sudo yum install python3 python3-pip

# 安装 Flask
pip3 install flask
```

</details>

## 🚀 快速开始

### 方式一：Systemd 服务（生产环境推荐）

```bash
# 克隆仓库
git clone https://github.com/yourusername/gpu-container-monitor.git
cd gpu-container-monitor

# 安装 systemd 服务
sudo cp gpu-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gpu-monitor
sudo systemctl start gpu-monitor

# 检查状态
sudo systemctl status gpu-monitor
```

**访问地址**：http://your-server-ip:5000

### 方式二：Docker 容器

```bash
# 克隆仓库
git clone https://github.com/yourusername/gpu-container-monitor.git
cd gpu-container-monitor

# 快速启动
./start-docker.sh

# 或手动启动
docker-compose up -d

# 查看日志
docker-compose logs -f
```

**访问地址**：http://your-server-ip:5001

### 方式三：手动运行（开发环境）

```bash
# 克隆仓库
git clone https://github.com/yourusername/gpu-container-monitor.git
cd gpu-container-monitor

# 安装依赖
pip3 install flask

# 运行
python3 app.py
```

**访问地址**：http://your-server-ip:5000

## 📖 使用说明

### Web 界面

1. 打开浏览器访问 `http://your-server-ip:5000`（Docker 版本为 5001）
2. 在顶部查看实时 GPU 指标
3. 在底部表格管理容器
4. 根据需要调整刷新间隔（1秒/3秒/5秒/10秒）

### 容器操作

- **▶ 启动**：启动已停止的容器
- **⏸ 暂停**：暂停运行中的容器（冻结进程）
- **▶ 恢复**：恢复已暂停的容器
- **🔄 重启**：重启容器
- **⏹ 停止**：停止运行中的容器

### 状态颜色

- 🟢 **健康运行**（深绿色）- 容器运行正常且通过健康检查
- 🟢 **运行中**（绿色）- 容器正常运行
- 🟠 **已暂停**（橙色）- 容器已暂停
- 🟡 **重启中**（黄色）- 容器正在重启
- 🔴 **已停止**（红色）- 容器已停止
- ⚪ **未启动**（灰色）- 容器已创建但未启动

## 🔧 配置

### Systemd 服务

编辑 `/etc/systemd/system/gpu-monitor.service`：

```ini
[Unit]
Description=GPU Container Monitor Service
After=network.target docker.service

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/gpu-container-monitor
ExecStart=/usr/bin/python3 /path/to/gpu-container-monitor/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Docker Compose

编辑 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  gpu-monitor:
    build: .
    container_name: gpu-container-monitor
    ports:
      - "5001:5000"  # 在此修改端口
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [utility]
    restart: unless-stopped
```

## 🛠️ 管理命令

### Systemd 服务

```bash
# 启动服务
sudo systemctl start gpu-monitor

# 停止服务
sudo systemctl stop gpu-monitor

# 重启服务
sudo systemctl restart gpu-monitor

# 查看状态
sudo systemctl status gpu-monitor

# 查看日志
sudo journalctl -u gpu-monitor -f

# 启用开机自启
sudo systemctl enable gpu-monitor

# 禁用开机自启
sudo systemctl disable gpu-monitor
```

### Docker 容器

```bash
# 启动容器
docker-compose up -d

# 停止容器
docker-compose down

# 重启容器
docker-compose restart

# 查看日志
docker-compose logs -f

# 重新构建镜像
docker-compose build

# 查看容器状态
docker-compose ps
```

## 🐛 故障排除

<details>
<summary><b>GPU 未检测到</b></summary>

```bash
# 检查 NVIDIA 驱动
nvidia-smi

# 检查 NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# 重启 Docker
sudo systemctl restart docker
```

</details>

<details>
<summary><b>容器未显示</b></summary>

```bash
# 检查 Docker socket 权限
ls -l /var/run/docker.sock

# 确保用户有 Docker 权限
sudo usermod -aG docker $USER

# 重启服务
sudo systemctl restart gpu-monitor
```

</details>

<details>
<summary><b>端口已被占用</b></summary>

```bash
# 检查占用端口的进程
sudo lsof -i :5000

# 在配置中更改端口
# Systemd：编辑 app.py
# Docker：编辑 docker-compose.yml
```

</details>

<details>
<summary><b>服务启动失败</b></summary>

```bash
# 查看日志
sudo journalctl -u gpu-monitor -n 50

# 检查 Python 依赖
pip3 install flask

# 验证文件权限
ls -l /path/to/gpu-container-monitor/app.py
```

</details>

## 📊 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                  Web 浏览器（端口 5000/5001）                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Flask Web 应用程序                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  GPU 信息    │  │   容器       │  │   控制       │     │
│  │  收集器      │  │   管理器     │  │   API        │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────┬────────────────────┬────────────────────┬─────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   nvidia-smi    │  │  Docker Socket  │  │  Docker CLI     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                      主机系统                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  GPU 0   │  │  GPU 1   │  │  GPU 2   │  │  GPU 3   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           具有 GPU 访问权限的 Docker 容器            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建您的特性分支（`git checkout -b feature/AmazingFeature`）
3. 提交您的更改（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 打开一个 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 使用 [Flask](https://flask.palletsprojects.com/) 构建
- 通过 [nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface) 进行 GPU 监控
- 通过 [Docker](https://www.docker.com/) 进行容器管理

## 📧 联系方式

- GitHub：[@yourusername](https://github.com/yourusername)
- 问题反馈：[GitHub Issues](https://github.com/yourusername/gpu-container-monitor/issues)

## 📱 关注我们

<div align="center">
  <img src="https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png" alt="微信公众号"/>
  <p><strong>👆 扫码关注，获取更多精彩内容</strong></p>
  <p>第一时间获取本项目及其他项目的最新动态！</p>
</div>

## ⭐ Star 历史

如果您觉得这个项目有用，请考虑给它一个 star！

---

为 GPU 计算社区用 ❤️ 制作
