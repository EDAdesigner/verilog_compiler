#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def test_compiler():
    # 测试示例文件
    test_files = ['examples/full_adder.v', 'examples/expression_test.v']
    
    for test_file in test_files:
        # 检查文件是否存在
        if not os.path.exists(test_file):
            print(f"错误: 测试文件 '{test_file}' 不存在")
            continue
            
        # 运行编译器
        print(f"测试文件: {test_file}")
        try:
            result = subprocess.run(['python', 'main.py', test_file], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    text=True)
            
            # 打印结果
            print("标准输出:")
            print(result.stdout)
            
            if result.stderr:
                print("错误输出:")
                print(result.stderr)
                
            # 检查是否生成了DOT和PNG文件
            base_name = os.path.splitext(test_file)[0]
            dot_file = f"{base_name}.dot"
            png_file = f"{base_name}.png"
            
            if os.path.exists(dot_file):
                print(f"✓ 成功生成DOT文件: {dot_file}")
            else:
                print(f"✗ 未能生成DOT文件: {dot_file}")
                
            if os.path.exists(png_file):
                print(f"✓ 成功生成PNG文件: {png_file}")
            else:
                print(f"✗ 未能生成PNG文件: {png_file}")
                
        except Exception as e:
            print(f"测试失败: {e}")
            
        print("-" * 50)
    
if __name__ == "__main__":
    test_compiler() 