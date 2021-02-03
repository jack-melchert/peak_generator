module coreir_shl #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 << in1;
endmodule

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

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module SHL (
    input [15:0] a,
    input [15:0] b,
    output [15:0] O0,
    output O1,
    output O2,
    output O3,
    output O4,
    output O5,
    input CLK
);
wire bit_const_0_None_out;
wire [15:0] const_0_16_out;
wire magma_Bits_16_eq_inst0_out;
wire [15:0] magma_Bits_16_shl_inst0_out;
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
coreir_eq #(
    .width(16)
) magma_Bits_16_eq_inst0 (
    .in0(magma_Bits_16_shl_inst0_out),
    .in1(const_0_16_out),
    .out(magma_Bits_16_eq_inst0_out)
);
coreir_shl #(
    .width(16)
) magma_Bits_16_shl_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_shl_inst0_out)
);
assign O0 = magma_Bits_16_shl_inst0_out;
assign O1 = bit_const_0_None_out;
assign O2 = magma_Bits_16_eq_inst0_out;
assign O3 = magma_Bits_16_shl_inst0_out[15];
assign O4 = bit_const_0_None_out;
assign O5 = bit_const_0_None_out;
endmodule

module PE (
    input [0:0] inst,
    input [31:0] inputs,
    input clk_en,
    output [15:0] O,
    input CLK
);
wire [15:0] SHL_inst0_O0;
wire SHL_inst0_O1;
wire SHL_inst0_O2;
wire SHL_inst0_O3;
wire SHL_inst0_O4;
wire SHL_inst0_O5;
SHL SHL_inst0 (
    .a(inputs[15:0]),
    .b(inputs[31:16]),
    .O0(SHL_inst0_O0),
    .O1(SHL_inst0_O1),
    .O2(SHL_inst0_O2),
    .O3(SHL_inst0_O3),
    .O4(SHL_inst0_O4),
    .O5(SHL_inst0_O5),
    .CLK(CLK)
);
assign O = SHL_inst0_O0;
endmodule

