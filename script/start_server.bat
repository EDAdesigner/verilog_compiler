@echo off
echo 启动Verilog编译器API服务器...

cd ..
python src/server.py

if errorlevel 1 (
    echo 服务器启动失败。
    exit /b 1
) 