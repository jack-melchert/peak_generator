module coreir_eq #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 == in1;
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module corebit_or (
    input in0,
    input in1,
    output out
);
  assign out = in0 | in1;
endmodule

module corebit_not (
    input in,
    output out
);
  assign out = ~in;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module corebit_and (
    input in0,
    input in1,
    output out
);
  assign out = in0 & in1;
endmodule

module ADD (
    input [15:0] a,
    input [15:0] b,
    output [15:0] O0,
    output O1,
    output O2,
    output O3,
    output O4,
    output O5,
    input CLK,
    input ASYNCRESET
);
wire bit_const_0_None_out;
wire [15:0] const_0_16_out;
wire [16:0] const_0_17_out;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_or_inst0_out;
wire magma_Bits_16_eq_inst0_out;
wire [16:0] magma_Bits_17_add_inst0_out;
wire [16:0] magma_Bits_17_add_inst1_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(16'h0000),
    .width(16)
) const_0_16 (
    .out(const_0_16_out)
);
coreir_const #(
    .value(17'h00000),
    .width(17)
) const_0_17 (
    .out(const_0_17_out)
);
corebit_and magma_Bit_and_inst0 (
    .in0(a[15]),
    .in1(b[15]),
    .out(magma_Bit_and_inst0_out)
);
corebit_and magma_Bit_and_inst1 (
    .in0(magma_Bit_and_inst0_out),
    .in1(magma_Bit_not_inst0_out),
    .out(magma_Bit_and_inst1_out)
);
corebit_and magma_Bit_and_inst2 (
    .in0(magma_Bit_not_inst1_out),
    .in1(magma_Bit_not_inst2_out),
    .out(magma_Bit_and_inst2_out)
);
corebit_and magma_Bit_and_inst3 (
    .in0(magma_Bit_and_inst2_out),
    .in1(magma_Bits_17_add_inst1_out[15]),
    .out(magma_Bit_and_inst3_out)
);
corebit_not magma_Bit_not_inst0 (
    .in(magma_Bits_17_add_inst1_out[15]),
    .out(magma_Bit_not_inst0_out)
);
corebit_not magma_Bit_not_inst1 (
    .in(a[15]),
    .out(magma_Bit_not_inst1_out)
);
corebit_not magma_Bit_not_inst2 (
    .in(b[15]),
    .out(magma_Bit_not_inst2_out)
);
corebit_or magma_Bit_or_inst0 (
    .in0(magma_Bit_and_inst1_out),
    .in1(magma_Bit_and_inst3_out),
    .out(magma_Bit_or_inst0_out)
);
coreir_eq #(
    .width(16)
) magma_Bits_16_eq_inst0 (
    .in0(magma_Bits_17_add_inst1_out[15:0]),
    .in1(const_0_16_out),
    .out(magma_Bits_16_eq_inst0_out)
);
wire [16:0] magma_Bits_17_add_inst0_in0;
assign magma_Bits_17_add_inst0_in0 = {bit_const_0_None_out,a[15:0]};
wire [16:0] magma_Bits_17_add_inst0_in1;
assign magma_Bits_17_add_inst0_in1 = {bit_const_0_None_out,b[15:0]};
coreir_add #(
    .width(17)
) magma_Bits_17_add_inst0 (
    .in0(magma_Bits_17_add_inst0_in0),
    .in1(magma_Bits_17_add_inst0_in1),
    .out(magma_Bits_17_add_inst0_out)
);
coreir_add #(
    .width(17)
) magma_Bits_17_add_inst1 (
    .in0(magma_Bits_17_add_inst0_out),
    .in1(const_0_17_out),
    .out(magma_Bits_17_add_inst1_out)
);
assign O0 = magma_Bits_17_add_inst1_out[15:0];
assign O1 = magma_Bits_17_add_inst1_out[16];
assign O2 = magma_Bits_16_eq_inst0_out;
assign O3 = magma_Bits_17_add_inst1_out[15];
assign O4 = magma_Bits_17_add_inst1_out[16];
assign O5 = magma_Bit_or_inst0_out;
endmodule

module PE (
    input [0:0] inst,
    input [31:0] inputs,
    input clk_en,
    output [15:0] O,
    input CLK,
    input ASYNCRESET
);
wire [15:0] ADD_inst0_O0;
wire ADD_inst0_O1;
wire ADD_inst0_O2;
wire ADD_inst0_O3;
wire ADD_inst0_O4;
wire ADD_inst0_O5;
ADD ADD_inst0 (
    .a(inputs[15:0]),
    .b(inputs[31:16]),
    .O0(ADD_inst0_O0),
    .O1(ADD_inst0_O1),
    .O2(ADD_inst0_O2),
    .O3(ADD_inst0_O3),
    .O4(ADD_inst0_O4),
    .O5(ADD_inst0_O5),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET)
);
assign O = ADD_inst0_O0;
endmodule

