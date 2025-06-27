module symbol_operations(
    a,
    b,
    c,
    d,
    y1,
    y2,
    y3,
    y4,
    y5,
    y6
);
    input [3:0] a;
    input [3:0] b;
    input [3:0] c;
    input [3:0] d;
    output [3:0] y1;
    output [3:0] y2;
    output [3:0] y3;
    output [3:0] y4;
    output [3:0] y5;
    output [3:0] y6;
    
    // 算术运算
    assign y1 = a + b;    // 加法
    assign y2 = c - d;    // 减法
    
    // 逻辑运算
    assign y3 = a & b;    // 按位与
    assign y4 = c | d;    // 按位或
    assign y5 = a ^ b;    // 按位异或
    
    // 比较运算
    assign y6 = (a > b) ? 4'b1111 : 4'b0000;  // 大于比较

endmodule 