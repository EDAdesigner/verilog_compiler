@echo off
echo Verilog编译器 - 转换Verilog到DOT图

if "%1"=="" (
    echo 用法: compile_verilog.bat 文件名.v
    exit /b 1
)

if not exist %1 (
    echo 错误: 找不到文件 %1
    exit /b 1
)

echo 正在编译 %1...
python main.py %1

if errorlevel 1 (
    echo 编译失败。
    exit /b 1
)

echo 编译完成。
echo.
echo 若要查看生成的图形，请使用图像查看器打开相应的.png文件。
echo. 