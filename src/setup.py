#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def setup():
    print("设置Verilog编译器环境...")
    
    # 创建examples目录
    if not os.path.exists('examples'):
        os.makedirs('examples')
        print("创建examples目录")
    
    # 创建示例文件
    setup_examples()
    
    # 安装依赖
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("安装依赖成功")
    except Exception as e:
        print(f"安装依赖失败: {e}")
        
    print("设置完成！")
    print("可以通过以下命令编译Verilog文件:")
    print("  python main.py examples/full_adder.v")
    print("或者使用批处理文件:")
    print("  compile_verilog.bat examples/full_adder.v")

def setup_examples():
    # 检查并确保示例目录中的文件存在
    examples = {
        'examples/full_adder.v': '''// 一位全加器
module full_adder(a, b, cin, sum, cout);
    input a;
    input b;
    input cin;
    output sum;
    output cout;
    
    wire s1;
    wire c1;
    wire c2;
    
    // 半加器1
    xor xor1(a, b, s1);
    and and1(a, b, c1);
    
    // 半加器2
    xor xor2(s1, cin, sum);
    and and2(s1, cin, c2);
    
    // 进位输出
    or or1(c1, c2, cout);
endmodule''',
        'examples/expression_test.v': '''// 表达式测试模块
module expression_test(a, b, c, d, out1, out2, out3);
    input a;
    input b;
    input c;
    input d;
    output out1;
    output out2;
    output out3;
    
    wire temp1;
    wire temp2;
    
    // 简单赋值
    assign temp1 = a & b;
    
    // 复杂表达式赋值
    assign temp2 = (a & b) | (c & d);
    
    // 一元运算符
    assign out1 = ~temp1;
    
    // 带括号的复杂表达式
    assign out2 = (a & b) | ~(c ^ d);
    
    // 混合运算符优先级测试
    assign out3 = a & b | c ^ d & ~(a | b) + c - d;
    
endmodule'''
    }
    
    for filename, content in examples.items():
        # 确保父目录存在
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # 写入文件内容
        with open(filename, 'w') as f:
            f.write(content)
        print(f"创建示例文件: {filename}")

if __name__ == "__main__":
    setup() 