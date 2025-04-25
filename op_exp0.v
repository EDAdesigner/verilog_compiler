module shared_exp(a, b, c, d, e, q);
    input a, b, c, d, e;
    output q;
    
    wire common_sum;
    assign common_sum = a + b;
    
    wire sum1, sum2, sum3;
    assign sum1 = common_sum + c;
    assign sum2 = common_sum + d;
    assign sum3 = common_sum + e;
    
    assign q = sum1 & sum2 & sum3;
endmodule