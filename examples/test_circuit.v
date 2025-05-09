// Test circuit - with multiplexer and adder
module test_circuit(a, b, c, sel, out1, out2);
    input a;       // Input A
    input b;       // Input B
    input c;       // Input C
    input sel;     // Select signal
    output out1;   // Output 1
    output out2;   // Output 2
    
    // Internal wires
    wire mux_out;  // Multiplexer output
    wire sum;      // Adder sum output
    wire carry;    // Adder carry output
    
    // Multiplexer - select a or b based on sel
    assign mux_out = sel ? b : a;
    
    // Half adder - compute sum and carry of mux_out and c
    xor xor1(mux_out, c, sum);
    and and1(mux_out, c, carry);
    
    // Output assignments
    assign out1 = sum;
    assign out2 = carry;
    
endmodule 