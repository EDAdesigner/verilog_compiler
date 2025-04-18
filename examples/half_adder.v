// Half adder module
module half_adder(a, b, sum, carry);
    input a;
    input b;
    output sum;
    output carry;
    
    // Gate level description
    xor xor1(a, b, sum);    // XOR gate for sum
    and and1(a, b, carry);  // AND gate for carry
    
endmodule