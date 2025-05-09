// 2-to-1 Multiplexer using assign statements
module multiplexer_assign(a, b, s, y);
    input a;    // Data input 0
    input b;    // Data input 1
    input s;    // Select input
    output y;   // Output
    
    // Behavioral description with assign statement
    assign y = s ? b : a;
    
endmodule 