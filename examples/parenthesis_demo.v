module parenthesis_demo(
    a,
    b,
    c,
    y1,
    y2
);
    input a;
    input b;
    input c;
    output y1;
    output y2;

    // 没有括号，& 优先级高于 |
    assign y1 = a | b & c;      // 实际等价于 a | (b & c)

    // 有括号，先算 a | b，再与 c 做与运算
    assign y2 = (a | b) & c;    // 强制先算 a | b

endmodule 