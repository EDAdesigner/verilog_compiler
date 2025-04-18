#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from verilog_parser import VerilogParser
from dot_generator import DotGenerator

def main():
    # 检查命令行参数
    if len(sys.argv) != 2:
        print("用法: python main.py <input_file.v>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"错误: 无法找到文件 '{input_file}'")
        sys.exit(1)
        
    # 检查文件扩展名
    if not input_file.lower().endswith('.v'):
        print(f"警告: 文件 '{input_file}' 不是以 .v 为扩展名的Verilog文件")
        
    # 读取输入文件
    try:
        with open(input_file, 'r') as f:
            verilog_code = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 '{input_file}': {e}")
        sys.exit(1)
        
    # 获取模块名（从文件名）
    module_name = os.path.splitext(os.path.basename(input_file))[0]
    
    # 解析Verilog代码
    parser = VerilogParser()
    try:
        module = parser.parse(verilog_code, module_name)
        if not module:
            print("错误: 解析模块失败")
            sys.exit(1)
    except Exception as e:
        print(f"错误: 解析Verilog代码时出错: {e}")
        sys.exit(1)
        
    # 生成DOT文件
    dot_generator = DotGenerator(module)
    try:
        dot = dot_generator.generate_dot()
        
        # 保存文件（使用相同的基本文件名）
        output_base = os.path.splitext(input_file)[0]
        dot_file, png_file = dot_generator.save(output_base)
        
        print(f"成功生成 DOT 文件: {dot_file}")
        print(f"成功生成图像文件: {png_file}")
        
    except Exception as e:
        print(f"错误: 生成 DOT 文件时出错: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    main() 