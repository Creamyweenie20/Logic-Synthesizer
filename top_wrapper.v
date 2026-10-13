module wrapper (input [15:0] sw, output [15:0] leds);

 top inst1 (.a(sw[0]), .b(sw[1]), .c(sw[2]), .d(sw[3]), .e(sw[4]), .f(sw[5]), .g(sw[6]), .out(leds[0]));
 assign leds[15:1] = 15'b0;
endmodule
