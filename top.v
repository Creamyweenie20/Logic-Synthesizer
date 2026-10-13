module top (a, b, c, d, e, f, g, out);
 input a, b, c, d, e, f, g;
 output out;
 wire w0, w1, d_n, w3, w4, w5, w6;

 and g0 (w0, f, g);
 and g1 (w1, e, f);
 not g2 (d_n, d);
 and g3 (w3, b, c, d_n);
 and g4 (w4, a, c, d);
 and g5 (w5, a, b);
 or g6 (w6, w0, w1, w3, w4, w5);
 buf g7 (out, w6);
endmodule
