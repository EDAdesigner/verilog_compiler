// 2-to-1 Multiplexer
module multiplexer(a, b, s, y);
    input a;    // Data input 0
    input b;    // Data input 1
    input s;    // Select input
    output y;   // Output
    
    // Internal wires
    wire not_s;
    wire and1_out;
    wire and2_out;
    
    // Gate level implementation
    not not1(s, not_s);
    and and1(a, not_s, and1_out);
    and and2(b, s, and2_out);
    or or1(and1_out, and2_out, y);
    
endmodule 