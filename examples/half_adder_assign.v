// Half adder module using assign statements
module half_adder_assign(a, b, sum, carry);
    input a;
    input b;
    output sum;
    output carry;
    
    // Behavioral description using assign statements
    assign sum = a ^ b;    // XOR operation for sum
    assign carry = a & b;  // AND operation for carry
    
endmodule 