#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from mux_generator import MuxGenerator

def main():
    # 创建输出目录
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 创建2选1多路选择器生成器
    generator = MuxGenerator("spmux")
    
    # 生成多路选择器
    dot = generator.generate_2to1_mux("$26")
    
    # 保存文件
    output_base = os.path.join(output_dir, "spmux")
    dot_file, png_file = generator.save(output_base)
    
    print(f"成功生成多路选择器图形:")
    print(f" - DOT文件: {dot_file}")
    print(f" - PNG文件: {png_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 