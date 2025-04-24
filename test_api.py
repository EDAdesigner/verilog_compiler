import requests
import os

# API服务器地址
API_URL = "http://localhost:8000"

def test_verilog_api():
    """
    测试普通Verilog解析API
    """
    test_code = """
    module full_adder(a, b, cin, sum, cout);
        input a, b, cin;
        output sum, cout;
        wire w1, w2, w3;
        
        and g1(w1, a, b);
        and g2(w2, a, cin);
        and g3(w3, b, cin);
        or g4(cout, w1, w2, w3);
        
        wire w4;
        xor g5(w4, a, b);
        xor g6(sum, w4, cin);
    endmodule
    """
    
    response = requests.post(
        f"{API_URL}/verilog",
        data={"verilog_code": test_code}
    )
    
    print("Verilog API测试结果:")
    print(response.json())
    
def test_optimize_api():
    """
    测试Verilog优化API
    """
    test_code = """
    module adder_with_shared_exprs(a, b, c, d, out1, out2);
        input a, b, c, d;
        output out1, out2;
        
        assign out1 = a & b + c & d;
        assign out2 = a & b + d;
    endmodule
    """
    
    response = requests.post(
        f"{API_URL}/optimize",
        data={"verilog_code": test_code}
    )
    
    print("优化API测试结果:")
    print(response.json())

if __name__ == "__main__":
    print("开始测试Verilog编译器API...")
    
    # 测试Verilog解析API
    test_verilog_api()
    
    # 测试Verilog优化API
    test_optimize_api()
    
    print("测试完成!") 