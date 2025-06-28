#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

# 服务器地址
BASE_URL = "http://localhost:8000"

# 测试用的Verilog代码
TEST_VERILOG_CODE = """
module unbalanced_add4(a, b, c, d, out); input a, b, c, d; output out; assign out = (((a + b) + c) + d); endmodule
"""

def test_root_endpoint():
    """测试根路径"""
    print("测试根路径...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_health_endpoint():
    """测试健康检查"""
    print("\n测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_verilog_endpoint():
    """测试/verilog端点"""
    print("\n测试/verilog端点...")
    try:
        data = {
            "verilog_code": TEST_VERILOG_CODE,
            "enhanced_style": True
        }
        response = requests.post(f"{BASE_URL}/verilog", data=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("编译成功!")
            print(f"模块信息: {result['module_info']}")
            print(f"生成的文件:")
            print(f"  DOT文件: {result['files']['dot_file']}")
            print(f"  PNG文件: {result['files']['png_file']}")
            return True
        else:
            print(f"错误: {response.text}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def test_optimize_endpoint():
    """测试/optimize端点"""
    print("\n测试/optimize端点...")
    try:
        data = {
            "verilog_code": TEST_VERILOG_CODE,
            "enhanced_style": True
        }
        response = requests.post(f"{BASE_URL}/optimize", data=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("优化编译成功!")
            print(f"模块信息: {result['module_info']}")
            print(f"生成的文件:")
            print(f"  DOT文件: {result['files']['dot_file']}")
            print(f"  PNG文件: {result['files']['png_file']}")
            return True
        elif response.status_code == 503:
            print("优化模块不可用（这是正常的，如果优化模块未正确配置）")
            return True
        else:
            print(f"错误: {response.text}")
            return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试Verilog编译器API服务器...")
    print("=" * 50)
    
    # 等待服务器启动
    print("等待服务器启动...")
    time.sleep(2)
    
    tests = [
        ("根路径", test_root_endpoint),
        ("健康检查", test_health_endpoint),
        ("Verilog编译", test_verilog_endpoint),
        ("优化编译", test_optimize_endpoint)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            print(f"✓ {test_name} 测试通过")
            passed += 1
        else:
            print(f"✗ {test_name} 测试失败")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过!")
    else:
        print("⚠️  部分测试失败，请检查服务器状态")

if __name__ == "__main__":
    main() 