module simple_precedence(
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

    // & 优先级高于 |
    assign y1 = a | b & c;   // 明确优先级：a | (b & c)
    // ~ 优先级高于 &
    assign y2 = ~a & b;      // 等价于 (~a) & b

endmodule