#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from graphviz import Digraph

def generate_spmux_image():
    """
    生成与图像中完全一致的多路选择器图形
    """
    # 创建输出目录
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 创建图形对象
    dot = Digraph('spmux_exact')
    dot.attr('graph', rankdir='LR', splines='ortho', nodesep='0.5')
    
    # 创建单个方框，包含所有内容
    label = '{{<A> A|<B> B|<S> S}|{$26\\nSpmux}|<Y> Y}'
    dot.node('spmux', label, shape='record', style='filled', fillcolor='white', fontname='Arial')
    
    # 添加方向箭头
    # 输入箭头
    dot.node('A_in', '', shape='point', style='invis')
    dot.node('B_in', '', shape='point', style='invis')
    dot.node('S_in', '', shape='point', style='invis')
    
    dot.edge('A_in', 'spmux:A', arrowhead='normal', arrowsize='0.7')
    dot.edge('B_in', 'spmux:B', arrowhead='normal', arrowsize='0.7')
    dot.edge('S_in', 'spmux:S', arrowhead='normal', arrowsize='0.7')
    
    # 输出箭头
    dot.node('Y_out', '', shape='point', style='invis')
    dot.edge('spmux:Y', 'Y_out', arrowhead='normal', arrowsize='0.7')
    
    # 保存文件
    output_base = os.path.join(output_dir, "spmux_exact")
    dot_file = f"{output_base}.dot"
    dot.save(dot_file)
    
    # 渲染并保存图片
    png_file = f"{output_base}.png"
    dot.render(output_base, format='png', cleanup=True)
    
    print(f"成功生成精确的多路选择器图形:")
    print(f" - DOT文件: {dot_file}")
    print(f" - PNG文件: {png_file}")
    
    return dot_file, png_file

def main():
    generate_spmux_image()
    return 0

if __name__ == "__main__":
    sys.exit(main()) 