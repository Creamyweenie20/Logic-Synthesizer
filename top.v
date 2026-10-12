module top (a, b, c, d, w6);
 input a, b, c, d;
 output w6;
 wire a_n, c_n, w2, w3, w4, w5;

 not g0 (a_n, a);
 not g1 (c_n, c);
 and g2 (w2, a_n, c_n);
 and g3 (w3, b);
 and g4 (w4, a, c);
 and g5 (w5, c_n, d);
 or g6 (w6, w2, w3, w4, w5);
endmodule
