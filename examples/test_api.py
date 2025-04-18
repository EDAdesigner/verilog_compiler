#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import webbrowser
import time

def test_verilog_api(verilog_code):
    """测试Verilog API，提交代码并打开生成的图像"""
    
    print("正在提交Verilog代码到API...")
    
    # API地址
    url = "http://localhost:8000/verilog"
    
    # 准备请求数据
    payload = {
        "code": verilog_code
    }
    
    try:
        # 发送请求
        response = requests.post(url, json=payload)
        
        # 检查响应
        if response.status_code == 200:
            data = response.json()
            print("API响应成功:")
            print(f"模块名: {data.get('module_name')}")
            print(f"DOT文件: {data.get('dot_file')}")
            print(f"PNG文件: {data.get('png_file')}")
            
            # 如果存在图像URL，则在浏览器中打开
            if 'png_url' in data:
                print(f"图像URL: {data.get('png_url')}")
                print("正在打开图像...")
                webbrowser.open(data['png_url'])
                return True
        else:
            print(f"API请求失败: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"发生错误: {e}")
    
    return False

if __name__ == "__main__":
    # 测试用的Verilog代码
    test_code = """
    module full_adder(a, b, cin, sum, cout);
      input a, b, cin;
      output sum, cout;
      
      wire w1, w2, w3;
      
      xor xor1(w1, a, b);
      xor xor2(sum, w1, cin);
      
      and and1(w2, a, b);
      and and2(w3, w1, cin);
      or or1(cout, w2, w3);
    endmodule
    """
    
    print("Verilog API测试脚本")
    print("-" * 50)
    
    # 检查服务器是否运行
    try:
        requests.get("http://localhost:8000")
        print("服务器已运行，正在执行测试...")
    except:
        print("无法连接到服务器，请确保服务器正在运行。")
        print("启动服务器命令: python server.py")
        exit(1)
    
    # 运行测试
    test_verilog_api(test_code) 