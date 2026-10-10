module top (a, b, c, w2);
 input a, b, c;
 output w2;
 wire a_n, w1;

 not g0 (a_n, a);
 and g1 (w1, a_n, b);
 or g2 (w2, w1, c);
endmodule
