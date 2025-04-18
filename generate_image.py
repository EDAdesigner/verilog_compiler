#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from graphviz import Source

def generate_image(dot_file):
    """从DOT文件生成图像，不依赖系统Graphviz"""
    try:
        # 读取DOT文件内容
        with open(dot_file, 'r') as f:
            dot_content = f.read()
        
        # 创建输出文件名
        base_name = os.path.splitext(dot_file)[0]
        output_file = f"{base_name}.png"
        
        # 使用graphviz库的Source直接渲染
        src = Source(dot_content, format='png')
        src.render(base_name, view=False, cleanup=True)
        
        print(f"成功生成图像文件: {output_file}")
        return True
    except Exception as e:
        print(f"错误: 生成图像文件时出错: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python generate_image.py <dot_file>")
        sys.exit(1)
    
    dot_file = sys.argv[1]
    if not os.path.exists(dot_file):
        print(f"错误: 找不到DOT文件 '{dot_file}'")
        sys.exit(1)
    
    if not generate_image(dot_file):
        sys.exit(1) 