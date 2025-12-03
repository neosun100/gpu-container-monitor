#!/bin/bash

echo "🐳 启动 GPU 容器监控 (Docker 版本)"
echo "================================"

cd "$(dirname "$0")"

# 停止旧容器
echo "停止旧容器..."
docker-compose down 2>/dev/null

# 构建并启动
echo "构建镜像..."
docker-compose build

echo "启动容器..."
docker-compose up -d

echo ""
echo "✅ 启动完成！"
echo ""
echo "📊 访问地址: http://10.68.2.212:5001"
echo "📋 查看日志: docker-compose logs -f"
echo "⏹  停止服务: docker-compose down"
echo ""
