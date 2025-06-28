#!/bin/bash

# Verilog编译器API服务器启动脚本

echo "启动Verilog编译器API服务器..."
echo "=================================="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖是否安装
echo "检查依赖..."
cd "$(dirname "$0")/src"

if ! python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    echo "安装依赖..."
    pip3 install -r requirements.txt
fi

# 启动服务器
echo "启动服务器..."
echo "服务器将在 http://localhost:8000 上运行"
echo "API文档可在 http://localhost:8000/docs 查看"
echo "按 Ctrl+C 停止服务器"
echo ""

python3 server.py 