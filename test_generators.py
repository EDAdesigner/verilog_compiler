#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from src.generate_mux import main as generate_mux
from src.generate_spmux import generate_spmux_image

def check_graphviz_installation():
    """检查Graphviz是否已安装"""
    try:
        subprocess.run(['dot', '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def test_verilog_compiler():
    """测试Verilog编译器和新的图形生成功能"""
    # 检查Graphviz是否已安装
    if not check_graphviz_installation():
        print("警告: Graphviz未安装或不在PATH中。图像生成功能可能无法正常工作。")
    
    print("=== 测试1: 原始Verilog编译器 ===")
    try:
        subprocess.run(['python', 'src/main.py', 'examples/half_adder.v'], check=True)
        print("半加器编译测试完成")
    except subprocess.CalledProcessError as e:
        print(f"错误: 半加器编译失败: {e}")
    
    print("\n=== 测试2: 多路选择器编译 ===")
    try:
        subprocess.run(['python', 'src/main.py', 'examples/multiplexer.v'], check=True)
        print("多路选择器编译测试完成")
    except subprocess.CalledProcessError as e:
        print(f"错误: 多路选择器编译失败: {e}")
    
    print("\n=== 测试3: 自定义多路选择器生成器 ===")
    try:
        generate_mux()
        print("自定义多路选择器生成器测试完成")
    except Exception as e:
        print(f"错误: 自定义多路选择器生成器失败: {e}")
    
    print("\n=== 测试4: 精确样式多路选择器生成器 ===")
    try:
        generate_spmux_image()
        print("精确样式多路选择器生成器测试完成")
    except Exception as e:
        print(f"错误: 精确样式多路选择器生成器失败: {e}")
    
    # 显示生成的文件
    print("\n=== 生成的文件 ===")
    try:
        if os.path.exists('output'):
            files = os.listdir('output')
            for file in files:
                if file.endswith('.png'):
                    print(f"- output/{file}")
    except Exception as e:
        print(f"错误: 无法列出生成的文件: {e}")

if __name__ == "__main__":
    test_verilog_compiler() 