# 🚀 GPU Container Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

> A beautiful, real-time monitoring dashboard for GPU-enabled Docker containers with comprehensive management capabilities.

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md)

![GPU Container Monitor Dashboard](https://via.placeholder.com/800x400/667eea/ffffff?text=GPU+Container+Monitor+Dashboard)

## ✨ Features

- 🎮 **Real-time GPU Monitoring** - Monitor all NVIDIA GPUs with live metrics
  - GPU utilization and memory usage
  - Temperature and power consumption
  - Visual progress bars for easy reading
  
- 📦 **Container Management** - Full control over GPU-enabled containers
  - Start, stop, pause, and restart containers
  - View container status with color-coded indicators
  - See which GPU each container is using
  
- 🎨 **Beautiful UI** - Modern, responsive web interface
  - Gradient color themes
  - Real-time updates (1s/3s/5s/10s intervals)
  - Status legend for quick reference
  - Mobile-friendly design
  
- 🔄 **Dual Deployment Options**
  - Systemd service (lightweight)
  - Docker container (isolated)
  
- 🌐 **Multi-language Support** - English, Chinese (Simplified/Traditional), Japanese

## 📋 Prerequisites

Before installation, ensure you have the following:

### Required

- **Operating System**: Linux (Ubuntu 20.04+, Debian 11+, or similar)
- **NVIDIA GPU**: One or more NVIDIA GPUs
- **NVIDIA Driver**: Version 450.80.02 or higher
- **nvidia-smi**: NVIDIA System Management Interface
- **Docker**: Version 20.10+ with NVIDIA Container Toolkit
- **Python**: Version 3.8 or higher

### Quick Check

Run this command to verify your system:

```bash
# Check NVIDIA driver and GPUs
nvidia-smi

# Check Docker
docker --version

# Check Python
python3 --version

# Check NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### Installation of Prerequisites

<details>
<summary><b>Ubuntu/Debian</b></summary>

```bash
# Install NVIDIA Driver (if not installed)
sudo apt update
sudo apt install nvidia-driver-535

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Install Python and pip
sudo apt install python3 python3-pip

# Install Flask
pip3 install flask
```

</details>

<details>
<summary><b>CentOS/RHEL</b></summary>

```bash
# Install NVIDIA Driver
sudo yum install nvidia-driver

# Install Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | \
  sudo tee /etc/yum.repos.d/nvidia-docker.repo

sudo yum install -y nvidia-container-toolkit
sudo systemctl restart docker

# Install Python and pip
sudo yum install python3 python3-pip

# Install Flask
pip3 install flask
```

</details>

## 🚀 Quick Start

### Option 1: Systemd Service (Recommended for Production)

```bash
# Clone the repository
git clone https://github.com/neosun100/gpu-container-monitor.git
cd gpu-container-monitor

# Install systemd service
sudo cp gpu-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gpu-monitor
sudo systemctl start gpu-monitor

# Check status
sudo systemctl status gpu-monitor
```

**Access**: http://your-server-ip:5000

### Option 2: Docker Container

```bash
# Clone the repository
git clone https://github.com/neosun100/gpu-container-monitor.git
cd gpu-container-monitor

# Quick start
./start-docker.sh

# Or manually
docker-compose up -d

# Check logs
docker-compose logs -f
```

**Access**: http://your-server-ip:5001

### Option 3: Manual Run (Development)

```bash
# Clone the repository
git clone https://github.com/neosun100/gpu-container-monitor.git
cd gpu-container-monitor

# Install dependencies
pip3 install flask

# Run
python3 app.py
```

**Access**: http://your-server-ip:5000

## 📖 Usage

### Web Interface

1. Open your browser and navigate to `http://your-server-ip:5000` (or 5001 for Docker)
2. View real-time GPU metrics in the top section
3. Manage containers in the bottom table
4. Adjust refresh interval (1s/3s/5s/10s) as needed

### Container Operations

- **▶ Start**: Start a stopped container
- **⏸ Pause**: Pause a running container (freezes processes)
- **▶ Resume**: Resume a paused container
- **🔄 Restart**: Restart a container
- **⏹ Stop**: Stop a running container

### Status Colors

- 🟢 **Healthy** (Deep Green) - Container running with health checks passing
- 🟢 **Running** (Green) - Container is running normally
- 🟠 **Paused** (Orange) - Container is paused
- 🟡 **Restarting** (Yellow) - Container is restarting
- 🔴 **Stopped** (Red) - Container has stopped
- ⚪ **Created** (Gray) - Container created but not started

## 🔧 Configuration

### Systemd Service

Edit `/etc/systemd/system/gpu-monitor.service`:

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

Edit `docker-compose.yml`:

```yaml
version: '3.8'

services:
  gpu-monitor:
    build: .
    container_name: gpu-container-monitor
    ports:
      - "5001:5000"  # Change port here
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

## 🛠️ Management Commands

### Systemd Service

```bash
# Start service
sudo systemctl start gpu-monitor

# Stop service
sudo systemctl stop gpu-monitor

# Restart service
sudo systemctl restart gpu-monitor

# View status
sudo systemctl status gpu-monitor

# View logs
sudo journalctl -u gpu-monitor -f

# Enable auto-start on boot
sudo systemctl enable gpu-monitor

# Disable auto-start
sudo systemctl disable gpu-monitor
```

### Docker Container

```bash
# Start container
docker-compose up -d

# Stop container
docker-compose down

# Restart container
docker-compose restart

# View logs
docker-compose logs -f

# Rebuild image
docker-compose build

# View container status
docker-compose ps
```

## 🐛 Troubleshooting

<details>
<summary><b>GPU not detected</b></summary>

```bash
# Check NVIDIA driver
nvidia-smi

# Check NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# Restart Docker
sudo systemctl restart docker
```

</details>

<details>
<summary><b>Containers not showing</b></summary>

```bash
# Check Docker socket permissions
ls -l /var/run/docker.sock

# Ensure user has Docker permissions
sudo usermod -aG docker $USER

# Restart service
sudo systemctl restart gpu-monitor
```

</details>

<details>
<summary><b>Port already in use</b></summary>

```bash
# Check what's using the port
sudo lsof -i :5000

# Change port in configuration
# For systemd: Edit app.py
# For Docker: Edit docker-compose.yml
```

</details>

<details>
<summary><b>Service fails to start</b></summary>

```bash
# Check logs
sudo journalctl -u gpu-monitor -n 50

# Check Python dependencies
pip3 install flask

# Verify file permissions
ls -l /path/to/gpu-container-monitor/app.py
```

</details>

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (Port 5000/5001)            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Flask Web Application                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   GPU Info   │  │  Container   │  │   Control    │     │
│  │   Collector  │  │   Manager    │  │   API        │     │
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
│                    Host System                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  GPU 0   │  │  GPU 1   │  │  GPU 2   │  │  GPU 3   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Docker Containers with GPU Access          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- GPU monitoring via [nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface)
- Container management via [Docker](https://www.docker.com/)

## 📧 Contact

- GitHub: [@neosun100](https://github.com/neosun100)
- Issues: [GitHub Issues](https://github.com/neosun100/gpu-container-monitor/issues)

## 📱 Follow Us

<div align="center">
  <img src="https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png" alt="WeChat Official Account"/>
  <p><strong>👆 Scan to follow for more exciting content</strong></p>
  <p>Get the latest updates on this and other projects!</p>
</div>

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

Made with ❤️ for the GPU computing community
