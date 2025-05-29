module dead_code_example(
    a,
    b,
    c,
    y
);
    input a;
    input b;
    input c;
    output y;
    wire w1;
    wire w2;
    wire w3;
    
    wire dead_w1;
    wire dead_w2;
    wire dead_w3;
    
    assign w1 = a & b;
    assign w2 = w1 | c;
    assign w3 = ~w2;
    assign y = w3;
    
    assign dead_w1 = a | b;        
    assign dead_w2 = dead_w1 & c;  
    assign dead_w3 = dead_w2 ^ a;  

endmodule 