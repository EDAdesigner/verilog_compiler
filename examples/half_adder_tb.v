// Half adder testbench
module half_adder_tb;
    // Inputs
    reg a;
    reg b;
    
    // Outputs
    wire sum;
    wire carry;
    
    // Instantiate the Unit Under Test (UUT)
    half_adder uut (
        .a(a),
        .b(b),
        .sum(sum),
        .carry(carry)
    );
    
    // Initialize inputs
    initial begin
        $monitor("Time=%0t a=%b b=%b sum=%b carry=%b", $time, a, b, sum, carry);
        
        // Test case 1: a=0, b=0
        a = 0; b = 0;
        #10;
        
        // Test case 2: a=0, b=1
        a = 0; b = 1;
        #10;
        
        // Test case 3: a=1, b=0
        a = 1; b = 0;
        #10;
        
        // Test case 4: a=1, b=1
        a = 1; b = 1;
        #10;
        
        $finish;
    end
endmodule 