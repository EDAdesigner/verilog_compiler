#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
from verilog_parser import VerilogParser
from dot_generator import DotGenerator
import argparse

def compile_verilog(input_file, optimize=False):
    """编译Verilog文件"""
    try:
        with open(input_file, 'r') as f:
            verilog_code = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 '{input_file}': {e}")
        return False

    # 获取模块名（从文件名）
    module_name = os.path.splitext(os.path.basename(input_file))[0]
    
    if optimize:
        # 使用优化版本的编译器
        try:
            # 导入优化版本的解析器
            from verilog_optimize.verilog_parser import VerilogParser as OptimizedParser
            from verilog_optimize.dot_generator import DotGenerator as OptimizedDotGenerator
            
            parser = OptimizedParser()
            module = parser.parse(verilog_code, module_name)
            
            if not module:
                print("错误: 解析模块失败")
                return False
                
            # 使用优化版本的dot生成器
            dot_generator = OptimizedDotGenerator(module)
            
        except ImportError as e:
            print(f"错误: 无法导入优化模块: {e}")
            return False
        except Exception as e:
            print(f"错误: 运行优化编译器时出错: {e}")
            return False
    else:
        # 使用原始版本的编译器
        try:
            parser = VerilogParser()
            module = parser.parse(verilog_code, module_name)
            
            if not module:
                print("错误: 解析模块失败")
                return False
                
            dot_generator = DotGenerator(module)
            
        except Exception as e:
            print(f"错误: 解析Verilog代码时出错: {e}")
            return False

    # 生成DOT文件
    try:
        dot = dot_generator.generate_dot()
        
        # 保存文件（使用相同的基本文件名）
        output_base = os.path.splitext(input_file)[0]
        if optimize:
            output_base += "_optimized"
        dot_file, png_file = dot_generator.save(output_base)
        
        print(f"成功生成 DOT 文件: {dot_file}")
        print(f"成功生成图像文件: {png_file}")
        
    except Exception as e:
        print(f"错误: 生成 DOT 文件时出错: {e}")
        return False

    return True

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='Verilog编译器')
    parser.add_argument('input_file', help='输入的Verilog文件(.v)')
    parser.add_argument('--optimize', '-o', action='store_true', help='启用共享子表达式优化')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.input_file):
        print(f"错误: 无法找到文件 '{args.input_file}'")
        sys.exit(1)
        
    # 检查文件扩展名
    if not args.input_file.lower().endswith('.v'):
        print(f"警告: 文件 '{args.input_file}' 不是以 .v 为扩展名的Verilog文件")
    
    # 编译文件
    if not compile_verilog(args.input_file, args.optimize):
        sys.exit(1)

if __name__ == "__main__":
    main() 