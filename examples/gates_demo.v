// 逻辑门演示模块
module gates_demo(a, b, c, and_out, or_out, not_out, nand_out, nor_out, xor_out, xnor_out);
    input a;
    input b;
    input c;
    output and_out;
    output or_out;
    output not_out;
    output nand_out;
    output nor_out;
    output xor_out;
    output xnor_out;

    // AND门演示
    and and1(a, b, and_out);
    
    // OR门演示
    or or1(a, b, or_out);
    
    // NOT门演示
    not not1(a, not_out);
    
    // NAND门演示
    nand nand1(a, b, nand_out);
    
    // NOR门演示
    nor nor1(a, b, nor_out);
    
    // XOR门演示
    xor xor1(a, b, xor_out);
    
    // XNOR门演示
    xnor xnor1(a, b, xnor_out);

endmodule