#!/bin/bash

echo "========================================"
echo "   校园校小助 UI 管理界面"
echo "========================================"
echo ""

# 启动本地服务器
echo "正在启动本地服务器..."
cd "$(dirname "$0")/ui"

# 检查 Python 版本
if command -v python3 &> /dev/null; then
    python3 -m http.server 8080 &
else
    echo "错误：未找到 Python3"
    exit 1
fi

SERVER_PID=$!

echo "服务器已启动: http://localhost:8080"
echo ""

# 等待服务器启动
sleep 2

# 打开浏览器
if command -v open &> /dev/null; then
    # macOS
    open http://localhost:8080
elif command -v xdg-open &> /dev/null; then
    # Linux
    xdg-open http://localhost:8080
elif command -v start &> /dev/null; then
    # Windows Git Bash
    start http://localhost:8080
fi

echo "浏览器已打开"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 等待用户中断
trap "echo '正在停止服务器...'; kill $SERVER_PID; exit" SIGINT SIGTERM
wait $SERVER_PID
