module shared_exp(a, b, c, d, e, q);
    input a, b, c, d, e;
    output q;
    
    wire not_a, not_b, common_or;
    assign not_a = ~a;           // 非门
    assign not_b = ~b;           // 非门
    assign common_or = a | b;    // 或门
    
    wire and1, or1, not1;
    assign and1 = common_or & c; // 与门
    assign or1 = common_or | d;  // 或门
    assign not1 = ~common_or;    // 非门
    
    assign q = (and1 | or1) & not1; // 复合逻辑：或、与、非组合
endmodule