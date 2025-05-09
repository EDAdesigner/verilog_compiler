#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def check_graphviz_installation():
    """检查Graphviz是否已安装"""
    try:
        subprocess.run(['dot', '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def test_enhanced_generator():
    """测试增强型电路图生成功能"""
    # 检查Graphviz是否已安装
    if not check_graphviz_installation():
        print("警告: Graphviz未安装或不在PATH中。图像生成功能可能无法正常工作。")
    
    # 创建输出目录
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    test_files = [
        "examples/half_adder.v",            # 半加器
        "examples/multiplexer.v",           # 多路选择器
        "examples/multiplexer_assign.v",    # 使用assign语句的多路选择器
        "examples/test_circuit.v"           # 混合电路
    ]
    
    print("=== 测试增强型电路图生成功能 ===")
    
    # 测试每个文件的增强型生成
    for test_file in test_files:
        if not os.path.exists(test_file):
            print(f"警告: 文件 '{test_file}' 不存在，跳过")
            continue
        
        module_name = os.path.splitext(os.path.basename(test_file))[0]
        print(f"\n测试文件: {test_file}")
        
        # 使用主程序处理文件
        try:
            cmd = ['python', 'src/main.py', test_file]
            print(f"执行命令: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"使用增强生成器处理 {module_name} 成功")
        except subprocess.CalledProcessError as e:
            print(f"错误: 使用增强生成器处理 {module_name} 失败: {e}")
        
        # 测试传统样式
        try:
            cmd = ['python', 'src/main.py', test_file, '--classic']
            print(f"执行命令: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"使用传统生成器处理 {module_name} 成功")
        except subprocess.CalledProcessError as e:
            print(f"错误: 使用传统生成器处理 {module_name} 失败: {e}")
            
        # 测试内部细节显示
        try:
            cmd = ['python', 'src/main.py', test_file, '--internal']
            print(f"执行命令: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"使用内部细节显示处理 {module_name} 成功")
        except subprocess.CalledProcessError as e:
            print(f"错误: 使用内部细节显示处理 {module_name} 失败: {e}")
    
    # 显示生成的文件
    print("\n=== 生成的文件 ===")
    try:
        files = os.listdir(output_dir)
        png_files = [f for f in files if f.endswith('.png')]
        
        if png_files:
            for file in sorted(png_files):
                print(f"- output/{file}")
        else:
            print("未找到生成的PNG文件")
    except Exception as e:
        print(f"错误: 无法列出生成的文件: {e}")

if __name__ == "__main__":
    test_enhanced_generator() 