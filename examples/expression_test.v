// 表达式测试模块
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
    
endmodule