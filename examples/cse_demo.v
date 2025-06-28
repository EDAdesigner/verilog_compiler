module cse_demo(
    a,
    b,
    c,
    y1,
    y2
);
    input a;
    input b;
    input c;
    output y1;
    output y2;

    assign y1 = (a & b) | c;
    assign y2 = (a & b) ^ c;

endmodule 