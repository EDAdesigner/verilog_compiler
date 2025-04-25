#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
from src.compiler.verilog_parser import VerilogParser, process_verilog
from src.optimizer.cse_optimizer import CSEOptimizer
from src.visualizer.dot_generator import DotGenerator
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
    if len(sys.argv) != 2:
        print("使用方法: python main.py <input_file.v>")
        return False
        
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        return False
        
    return process_verilog(input_file)

if __name__ == "__main__":
    main() 