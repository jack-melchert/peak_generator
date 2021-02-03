module coreir_xor #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 ^ in1;
endmodule

module coreir_or #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 | in1;
endmodule

module coreir_mux #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    input sel,
    output [width-1:0] out
);
  assign out = sel ? in1 : in0;
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

module coreir_and #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 & in1;
endmodule

module corebit_const #(
    parameter value = 1
) (
    output out
);
  assign out = value;
endmodule

module commonlib_muxn__N2__width16 (
    input [15:0] in_data [1:0],
    input [0:0] in_sel,
    output [15:0] out
);
wire [15:0] _join_out;
coreir_mux #(
    .width(16)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module commonlib_muxn__N2__width1 (
    input [0:0] in_data [1:0],
    input [0:0] in_sel,
    output [0:0] out
);
wire [0:0] _join_out;
coreir_mux #(
    .width(1)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
endmodule

module Mux2xOutUInt16 (
    input [15:0] I0,
    input [15:0] I1,
    input S,
    output [15:0] O
);
wire [15:0] coreir_commonlib_mux2x16_inst0_out;
wire [15:0] coreir_commonlib_mux2x16_inst0_in_data [1:0];
assign coreir_commonlib_mux2x16_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x16_inst0_in_data[0] = I0;
commonlib_muxn__N2__width16 coreir_commonlib_mux2x16_inst0 (
    .in_data(coreir_commonlib_mux2x16_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x16_inst0_out)
);
assign O = coreir_commonlib_mux2x16_inst0_out;
endmodule

module Mux2xOutBit (
    input I0,
    input I1,
    input S,
    output O
);
wire [0:0] coreir_commonlib_mux2x1_inst0_out;
wire [0:0] coreir_commonlib_mux2x1_inst0_in_data [1:0];
assign coreir_commonlib_mux2x1_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x1_inst0_in_data[0] = I0;
commonlib_muxn__N2__width1 coreir_commonlib_mux2x1_inst0 (
    .in_data(coreir_commonlib_mux2x1_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x1_inst0_out)
);
assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module BIT_ALU (
    input [1:0] alu,
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
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_O;
wire [15:0] Mux2xOutUInt16_inst0_O;
wire [15:0] Mux2xOutUInt16_inst1_O;
wire bit_const_0_None_out;
wire [15:0] const_0_16_out;
wire [1:0] const_0_2_out;
wire [1:0] const_1_2_out;
wire [15:0] magma_Bits_16_and_inst0_out;
wire magma_Bits_16_eq_inst0_out;
wire [15:0] magma_Bits_16_or_inst0_out;
wire [15:0] magma_Bits_16_xor_inst0_out;
wire magma_Bits_2_eq_inst0_out;
wire magma_Bits_2_eq_inst1_out;
wire magma_Bits_2_eq_inst2_out;
wire magma_Bits_2_eq_inst3_out;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(bit_const_0_None_out),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_2_eq_inst1_out),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(Mux2xOutBit_inst0_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_2_eq_inst3_out),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(magma_Bits_16_xor_inst0_out),
    .I1(magma_Bits_16_or_inst0_out),
    .S(magma_Bits_2_eq_inst0_out),
    .O(Mux2xOutUInt16_inst0_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst1 (
    .I0(Mux2xOutUInt16_inst0_O),
    .I1(magma_Bits_16_and_inst0_out),
    .S(magma_Bits_2_eq_inst2_out),
    .O(Mux2xOutUInt16_inst1_O)
);
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
    .value(2'h0),
    .width(2)
) const_0_2 (
    .out(const_0_2_out)
);
coreir_const #(
    .value(2'h1),
    .width(2)
) const_1_2 (
    .out(const_1_2_out)
);
coreir_and #(
    .width(16)
) magma_Bits_16_and_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_and_inst0_out)
);
coreir_eq #(
    .width(16)
) magma_Bits_16_eq_inst0 (
    .in0(Mux2xOutUInt16_inst1_O),
    .in1(const_0_16_out),
    .out(magma_Bits_16_eq_inst0_out)
);
coreir_or #(
    .width(16)
) magma_Bits_16_or_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_or_inst0_out)
);
coreir_xor #(
    .width(16)
) magma_Bits_16_xor_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_xor_inst0_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst0 (
    .in0(alu),
    .in1(const_0_2_out),
    .out(magma_Bits_2_eq_inst0_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst1 (
    .in0(alu),
    .in1(const_0_2_out),
    .out(magma_Bits_2_eq_inst1_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst2 (
    .in0(alu),
    .in1(const_1_2_out),
    .out(magma_Bits_2_eq_inst2_out)
);
coreir_eq #(
    .width(2)
) magma_Bits_2_eq_inst3 (
    .in0(alu),
    .in1(const_1_2_out),
    .out(magma_Bits_2_eq_inst3_out)
);
assign O0 = Mux2xOutUInt16_inst1_O;
assign O1 = Mux2xOutBit_inst1_O;
assign O2 = magma_Bits_16_eq_inst0_out;
assign O3 = Mux2xOutUInt16_inst1_O[15];
assign O4 = bit_const_0_None_out;
assign O5 = bit_const_0_None_out;
endmodule

module PE (
    input [1:0] inst,
    input [31:0] inputs,
    input clk_en,
    output [15:0] O,
    input CLK
);
wire [15:0] BIT_ALU_inst0_O0;
wire BIT_ALU_inst0_O1;
wire BIT_ALU_inst0_O2;
wire BIT_ALU_inst0_O3;
wire BIT_ALU_inst0_O4;
wire BIT_ALU_inst0_O5;
BIT_ALU BIT_ALU_inst0 (
    .alu(inst),
    .a(inputs[15:0]),
    .b(inputs[31:16]),
    .O0(BIT_ALU_inst0_O0),
    .O1(BIT_ALU_inst0_O1),
    .O2(BIT_ALU_inst0_O2),
    .O3(BIT_ALU_inst0_O3),
    .O4(BIT_ALU_inst0_O4),
    .O5(BIT_ALU_inst0_O5),
    .CLK(CLK)
);
assign O = BIT_ALU_inst0_O0;
endmodule

