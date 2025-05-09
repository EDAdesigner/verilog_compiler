#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
from verilog_parser import VerilogParser
from dot_generator import DotGenerator
from new_dot_generator import EnhancedDotGenerator
import argparse

def compile_verilog(input_file, optimize=False, enhanced_style=True, show_internal=False):
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
            
            parser = OptimizedParser()
            module = parser.parse(verilog_code, module_name)
            
            if not module:
                print("错误: 解析模块失败")
                return False
                
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
                
        except Exception as e:
            print(f"错误: 解析Verilog代码时出错: {e}")
            return False

    # 生成DOT文件
    try:
        # 创建输出目录（如果不存在）
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存文件到输出目录
        output_base = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0])
        if optimize:
            output_base += "_optimized"
            
        # 使用增强型图形生成器
        if enhanced_style:
            dot_generator = EnhancedDotGenerator(module)
            # 设置是否显示内部细节
            dot_generator.set_show_internal(show_internal)
            # 根据模块类型自动检测和设置样式
            if hasattr(module, 'name'):
                if 'mux' in module.name.lower() or 'select' in module.name.lower():
                    print("检测到多路选择器，使用专用样式...")
                    dot_generator.set_style('mux')
                elif 'adder' in module.name.lower():
                    print("检测到加法器，使用专用样式...")
                    dot_generator.set_style('adder')
            dot = dot_generator.generate_dot()
            dot_file, png_file = dot_generator.save(output_base)
        else:
            # 使用传统图形生成器
            dot_generator = DotGenerator(module)
            dot = dot_generator.generate_dot()
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
    parser.add_argument('--classic', '-c', action='store_true', help='使用传统图形样式（默认使用增强样式）')
    parser.add_argument('--internal', '-i', action='store_true', help='显示电路内部细节（门级实现）')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.input_file):
        print(f"错误: 无法找到文件 '{args.input_file}'")
        sys.exit(1)
        
    # 检查文件扩展名
    if not args.input_file.lower().endswith('.v'):
        print(f"警告: 文件 '{args.input_file}' 不是以 .v 为扩展名的Verilog文件")
    
    # 编译文件
    if not compile_verilog(args.input_file, args.optimize, not args.classic, args.internal):
        sys.exit(1)

if __name__ == "__main__":
    main() 