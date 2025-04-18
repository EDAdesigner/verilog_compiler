// 一位全加器
module full_adder(a, b, cin, sum, cout);
    input a;
    input b;
    input cin;
    output sum;
    output cout;
    
    wire s1;
    wire c1;
    wire c2;
    
    // 半加器1
    xor xor1(a, b, s1);
    and and1(a, b, c1);
    
    // 半加器2
    xor xor2(s1, cin, sum);
    and and2(s1, cin, c2);
    
    // 进位输出
    or or1(c1, c2, cout);
endmodule