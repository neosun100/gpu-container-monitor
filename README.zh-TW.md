# 🚀 GPU 容器監控系統

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

> 一個美觀的、即時的 GPU 容器監控儀表板，具有全面的管理功能。

[English](README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md)

![GPU 容器監控儀表板](https://via.placeholder.com/800x400/667eea/ffffff?text=GPU+Container+Monitor+Dashboard)

## ✨ 功能特性

- 🎮 **即時 GPU 監控** - 監控所有 NVIDIA GPU 的即時指標
  - GPU 利用率和顯存使用
  - 溫度和功耗
  - 視覺化進度條，易於閱讀
  
- 📦 **容器管理** - 完全控制使用 GPU 的容器
  - 啟動、停止、暫停和重啟容器
  - 彩色狀態指示器查看容器狀態
  - 查看每個容器使用的 GPU
  
- 🎨 **精美介面** - 現代化、響應式 Web 介面
  - 漸變色主題
  - 即時更新（1秒/3秒/5秒/10秒間隔）
  - 狀態圖例快速參考
  - 行動裝置友善設計
  
- 🔄 **雙重部署選項**
  - Systemd 服務（輕量級）
  - Docker 容器（隔離環境）
  
- 🌐 **多語言支援** - 英語、簡體中文、繁體中文、日語

## 📋 前置要求

安裝前，請確保您具備以下條件：

### 必需項

- **作業系統**：Linux（Ubuntu 20.04+、Debian 11+ 或類似系統）
- **NVIDIA GPU**：一個或多個 NVIDIA GPU
- **NVIDIA 驅動程式**：版本 450.80.02 或更高
- **nvidia-smi**：NVIDIA 系統管理介面
- **Docker**：版本 20.10+ 並安裝 NVIDIA Container Toolkit
- **Python**：版本 3.8 或更高

### 快速檢查

執行此命令驗證您的系統：

```bash
# 檢查 NVIDIA 驅動程式和 GPU
nvidia-smi

# 檢查 Docker
docker --version

# 檢查 Python
python3 --version

# 檢查 NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### 安裝前置依賴

<details>
<summary><b>Ubuntu/Debian</b></summary>

```bash
# 安裝 NVIDIA 驅動程式（如果未安裝）
sudo apt update
sudo apt install nvidia-driver-535

# 安裝 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安裝 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 安裝 Python 和 pip
sudo apt install python3 python3-pip

# 安裝 Flask
pip3 install flask
```

</details>

<details>
<summary><b>CentOS/RHEL</b></summary>

```bash
# 安裝 NVIDIA 驅動程式
sudo yum install nvidia-driver

# 安裝 Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io

# 安裝 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.repo | \
  sudo tee /etc/yum.repos.d/nvidia-docker.repo

sudo yum install -y nvidia-container-toolkit
sudo systemctl restart docker

# 安裝 Python 和 pip
sudo yum install python3 python3-pip

# 安裝 Flask
pip3 install flask
```

</details>

## 🚀 快速開始

### 方式一：Systemd 服務（生產環境推薦）

```bash
# 複製儲存庫
git clone https://github.com/neosun100/gpu-container-monitor.git
cd gpu-container-monitor

# 安裝 systemd 服務
sudo cp gpu-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gpu-monitor
sudo systemctl start gpu-monitor

# 檢查狀態
sudo systemctl status gpu-monitor
```

**存取位址**：http://your-server-ip:5000

### 方式二：Docker 容器

```bash
# 複製儲存庫
git clone https://github.com/neosun100/gpu-container-monitor.git
cd gpu-container-monitor

# 快速啟動
./start-docker.sh

# 或手動啟動
docker-compose up -d

# 查看日誌
docker-compose logs -f
```

**存取位址**：http://your-server-ip:5001

### 方式三：手動執行（開發環境）

```bash
# 複製儲存庫
git clone https://github.com/neosun100/gpu-container-monitor.git
cd gpu-container-monitor

# 安裝依賴
pip3 install flask

# 執行
python3 app.py
```

**存取位址**：http://your-server-ip:5000

## 📖 使用說明

### Web 介面

1. 開啟瀏覽器存取 `http://your-server-ip:5000`（Docker 版本為 5001）
2. 在頂部查看即時 GPU 指標
3. 在底部表格管理容器
4. 根據需要調整重新整理間隔（1秒/3秒/5秒/10秒）

### 容器操作

- **▶ 啟動**：啟動已停止的容器
- **⏸ 暫停**：暫停執行中的容器（凍結程序）
- **▶ 恢復**：恢復已暫停的容器
- **🔄 重啟**：重啟容器
- **⏹ 停止**：停止執行中的容器

### 狀態顏色

- 🟢 **健康執行**（深綠色）- 容器執行正常且通過健康檢查
- 🟢 **執行中**（綠色）- 容器正常執行
- 🟠 **已暫停**（橙色）- 容器已暫停
- 🟡 **重啟中**（黃色）- 容器正在重啟
- 🔴 **已停止**（紅色）- 容器已停止
- ⚪ **未啟動**（灰色）- 容器已建立但未啟動

## 🔧 設定

### Systemd 服務

編輯 `/etc/systemd/system/gpu-monitor.service`：

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

編輯 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  gpu-monitor:
    build: .
    container_name: gpu-container-monitor
    ports:
      - "5001:5000"  # 在此修改連接埠
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

### Systemd 服務

```bash
# 啟動服務
sudo systemctl start gpu-monitor

# 停止服務
sudo systemctl stop gpu-monitor

# 重啟服務
sudo systemctl restart gpu-monitor

# 查看狀態
sudo systemctl status gpu-monitor

# 查看日誌
sudo journalctl -u gpu-monitor -f

# 啟用開機自動啟動
sudo systemctl enable gpu-monitor

# 停用開機自動啟動
sudo systemctl disable gpu-monitor
```

### Docker 容器

```bash
# 啟動容器
docker-compose up -d

# 停止容器
docker-compose down

# 重啟容器
docker-compose restart

# 查看日誌
docker-compose logs -f

# 重新建置映像
docker-compose build

# 查看容器狀態
docker-compose ps
```

## 🐛 故障排除

<details>
<summary><b>GPU 未偵測到</b></summary>

```bash
# 檢查 NVIDIA 驅動程式
nvidia-smi

# 檢查 NVIDIA Container Toolkit
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# 重新啟動 Docker
sudo systemctl restart docker
```

</details>

<details>
<summary><b>容器未顯示</b></summary>

```bash
# 檢查 Docker socket 權限
ls -l /var/run/docker.sock

# 確保使用者有 Docker 權限
sudo usermod -aG docker $USER

# 重新啟動服務
sudo systemctl restart gpu-monitor
```

</details>

<details>
<summary><b>連接埠已被佔用</b></summary>

```bash
# 檢查佔用連接埠的程序
sudo lsof -i :5000

# 在設定中變更連接埠
# Systemd：編輯 app.py
# Docker：編輯 docker-compose.yml
```

</details>

<details>
<summary><b>服務啟動失敗</b></summary>

```bash
# 查看日誌
sudo journalctl -u gpu-monitor -n 50

# 檢查 Python 依賴
pip3 install flask

# 驗證檔案權限
ls -l /path/to/gpu-container-monitor/app.py
```

</details>

## 📊 架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                  Web 瀏覽器（連接埠 5000/5001）              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Flask Web 應用程式                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  GPU 資訊    │  │   容器       │  │   控制       │     │
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
│                      主機系統                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  GPU 0   │  │  GPU 1   │  │  GPU 2   │  │  GPU 3   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           具有 GPU 存取權限的 Docker 容器            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🤝 貢獻

歡迎貢獻！請隨時提交 Pull Request。

1. Fork 本儲存庫
2. 建立您的功能分支（`git checkout -b feature/AmazingFeature`）
3. 提交您的變更（`git commit -m 'Add some AmazingFeature'`）
4. 推送到分支（`git push origin feature/AmazingFeature`）
5. 開啟一個 Pull Request

## 📝 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案。

## 🙏 致謝

- 使用 [Flask](https://flask.palletsprojects.com/) 建置
- 透過 [nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface) 進行 GPU 監控
- 透過 [Docker](https://www.docker.com/) 進行容器管理

## 📧 聯絡方式

- GitHub：[@neosun100](https://github.com/neosun100)
- 問題回報：[GitHub Issues](https://github.com/neosun100/gpu-container-monitor/issues)

## 📱 關注我們

<div align="center">
  <img src="https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png" alt="微信公眾號"/>
  <p><strong>👆 掃碼關注，獲取更多精彩內容</strong></p>
  <p>第一時間獲取本專案及其他專案的最新動態！</p>
</div>

## ⭐ Star 歷史

如果您覺得這個專案有用，請考慮給它一個 star！

---

為 GPU 運算社群用 ❤️ 製作
