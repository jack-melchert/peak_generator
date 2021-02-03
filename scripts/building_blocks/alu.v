module coreir_xor #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 ^ in1;
endmodule

module coreir_ule #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 <= in1;
endmodule

module coreir_uge #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = in0 >= in1;
endmodule

module coreir_slt #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = $signed(in0) < $signed(in1);
endmodule

module coreir_sle #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = $signed(in0) <= $signed(in1);
endmodule

module coreir_shl #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 << in1;
endmodule

module coreir_sge #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output out
);
  assign out = $signed(in0) >= $signed(in1);
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

module coreir_not #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = ~in;
endmodule

module coreir_neg #(
    parameter width = 1
) (
    input [width-1:0] in,
    output [width-1:0] out
);
  assign out = -in;
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

module coreir_lshr #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 >> in1;
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

module coreir_ashr #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = $signed(in0) >>> in1;
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

module coreir_add #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 + in1;
endmodule

module corebit_xor (
    input in0,
    input in1,
    output out
);
  assign out = in0 ^ in1;
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

module Mux2xBit (
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

module Cond (
    input [4:0] code,
    input alu,
    input Z,
    input N,
    input C,
    input V,
    output O,
    input CLK
);
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst10_O;
wire Mux2xOutBit_inst11_O;
wire Mux2xOutBit_inst12_O;
wire Mux2xOutBit_inst13_O;
wire Mux2xOutBit_inst14_O;
wire Mux2xOutBit_inst15_O;
wire Mux2xOutBit_inst16_O;
wire Mux2xOutBit_inst17_O;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst3_O;
wire Mux2xOutBit_inst4_O;
wire Mux2xOutBit_inst5_O;
wire Mux2xOutBit_inst6_O;
wire Mux2xOutBit_inst7_O;
wire Mux2xOutBit_inst8_O;
wire Mux2xOutBit_inst9_O;
wire [4:0] const_0_5_out;
wire [4:0] const_10_5_out;
wire [4:0] const_11_5_out;
wire [4:0] const_12_5_out;
wire [4:0] const_13_5_out;
wire [4:0] const_14_5_out;
wire [4:0] const_15_5_out;
wire [4:0] const_16_5_out;
wire [4:0] const_17_5_out;
wire [4:0] const_1_5_out;
wire [4:0] const_2_5_out;
wire [4:0] const_3_5_out;
wire [4:0] const_4_5_out;
wire [4:0] const_5_5_out;
wire [4:0] const_6_5_out;
wire [4:0] const_7_5_out;
wire [4:0] const_8_5_out;
wire [4:0] const_9_5_out;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst10_out;
wire magma_Bit_not_inst11_out;
wire magma_Bit_not_inst12_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_not_inst3_out;
wire magma_Bit_not_inst4_out;
wire magma_Bit_not_inst5_out;
wire magma_Bit_not_inst6_out;
wire magma_Bit_not_inst7_out;
wire magma_Bit_not_inst8_out;
wire magma_Bit_not_inst9_out;
wire magma_Bit_or_inst0_out;
wire magma_Bit_or_inst1_out;
wire magma_Bit_or_inst2_out;
wire magma_Bit_or_inst3_out;
wire magma_Bit_or_inst4_out;
wire magma_Bit_or_inst5_out;
wire magma_Bit_xor_inst0_out;
wire magma_Bit_xor_inst1_out;
wire magma_Bit_xor_inst2_out;
wire magma_Bit_xor_inst3_out;
wire magma_Bits_5_eq_inst0_out;
wire magma_Bits_5_eq_inst1_out;
wire magma_Bits_5_eq_inst10_out;
wire magma_Bits_5_eq_inst11_out;
wire magma_Bits_5_eq_inst12_out;
wire magma_Bits_5_eq_inst13_out;
wire magma_Bits_5_eq_inst14_out;
wire magma_Bits_5_eq_inst15_out;
wire magma_Bits_5_eq_inst16_out;
wire magma_Bits_5_eq_inst17_out;
wire magma_Bits_5_eq_inst18_out;
wire magma_Bits_5_eq_inst19_out;
wire magma_Bits_5_eq_inst2_out;
wire magma_Bits_5_eq_inst3_out;
wire magma_Bits_5_eq_inst4_out;
wire magma_Bits_5_eq_inst5_out;
wire magma_Bits_5_eq_inst6_out;
wire magma_Bits_5_eq_inst7_out;
wire magma_Bits_5_eq_inst8_out;
wire magma_Bits_5_eq_inst9_out;
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(magma_Bit_and_inst3_out),
    .I1(magma_Bit_or_inst3_out),
    .S(magma_Bits_5_eq_inst19_out),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(Mux2xOutBit_inst0_O),
    .I1(magma_Bit_and_inst2_out),
    .S(magma_Bits_5_eq_inst18_out),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutBit Mux2xOutBit_inst10 (
    .I0(Mux2xOutBit_inst9_O),
    .I1(magma_Bit_not_inst3_out),
    .S(magma_Bits_5_eq_inst9_out),
    .O(Mux2xOutBit_inst10_O)
);
Mux2xOutBit Mux2xOutBit_inst11 (
    .I0(Mux2xOutBit_inst10_O),
    .I1(V),
    .S(magma_Bits_5_eq_inst8_out),
    .O(Mux2xOutBit_inst11_O)
);
Mux2xOutBit Mux2xOutBit_inst12 (
    .I0(Mux2xOutBit_inst11_O),
    .I1(magma_Bit_not_inst2_out),
    .S(magma_Bits_5_eq_inst7_out),
    .O(Mux2xOutBit_inst12_O)
);
Mux2xOutBit Mux2xOutBit_inst13 (
    .I0(Mux2xOutBit_inst12_O),
    .I1(N),
    .S(magma_Bits_5_eq_inst6_out),
    .O(Mux2xOutBit_inst13_O)
);
Mux2xOutBit Mux2xOutBit_inst14 (
    .I0(Mux2xOutBit_inst13_O),
    .I1(magma_Bit_not_inst1_out),
    .S(magma_Bit_or_inst5_out),
    .O(Mux2xOutBit_inst14_O)
);
Mux2xOutBit Mux2xOutBit_inst15 (
    .I0(Mux2xOutBit_inst14_O),
    .I1(C),
    .S(magma_Bit_or_inst4_out),
    .O(Mux2xOutBit_inst15_O)
);
Mux2xOutBit Mux2xOutBit_inst16 (
    .I0(Mux2xOutBit_inst15_O),
    .I1(magma_Bit_not_inst0_out),
    .S(magma_Bits_5_eq_inst1_out),
    .O(Mux2xOutBit_inst16_O)
);
Mux2xOutBit Mux2xOutBit_inst17 (
    .I0(Mux2xOutBit_inst16_O),
    .I1(Z),
    .S(magma_Bits_5_eq_inst0_out),
    .O(Mux2xOutBit_inst17_O)
);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(Mux2xOutBit_inst1_O),
    .I1(magma_Bit_or_inst2_out),
    .S(magma_Bits_5_eq_inst17_out),
    .O(Mux2xOutBit_inst2_O)
);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(Mux2xOutBit_inst2_O),
    .I1(alu),
    .S(magma_Bits_5_eq_inst16_out),
    .O(Mux2xOutBit_inst3_O)
);
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(Mux2xOutBit_inst3_O),
    .I1(magma_Bit_or_inst1_out),
    .S(magma_Bits_5_eq_inst15_out),
    .O(Mux2xOutBit_inst4_O)
);
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(Mux2xOutBit_inst4_O),
    .I1(magma_Bit_and_inst1_out),
    .S(magma_Bits_5_eq_inst14_out),
    .O(Mux2xOutBit_inst5_O)
);
Mux2xOutBit Mux2xOutBit_inst6 (
    .I0(Mux2xOutBit_inst5_O),
    .I1(magma_Bit_xor_inst1_out),
    .S(magma_Bits_5_eq_inst13_out),
    .O(Mux2xOutBit_inst6_O)
);
Mux2xOutBit Mux2xOutBit_inst7 (
    .I0(Mux2xOutBit_inst6_O),
    .I1(magma_Bit_not_inst6_out),
    .S(magma_Bits_5_eq_inst12_out),
    .O(Mux2xOutBit_inst7_O)
);
Mux2xOutBit Mux2xOutBit_inst8 (
    .I0(Mux2xOutBit_inst7_O),
    .I1(magma_Bit_or_inst0_out),
    .S(magma_Bits_5_eq_inst11_out),
    .O(Mux2xOutBit_inst8_O)
);
Mux2xOutBit Mux2xOutBit_inst9 (
    .I0(Mux2xOutBit_inst8_O),
    .I1(magma_Bit_and_inst0_out),
    .S(magma_Bits_5_eq_inst10_out),
    .O(Mux2xOutBit_inst9_O)
);
coreir_const #(
    .value(5'h00),
    .width(5)
) const_0_5 (
    .out(const_0_5_out)
);
coreir_const #(
    .value(5'h0a),
    .width(5)
) const_10_5 (
    .out(const_10_5_out)
);
coreir_const #(
    .value(5'h0b),
    .width(5)
) const_11_5 (
    .out(const_11_5_out)
);
coreir_const #(
    .value(5'h0c),
    .width(5)
) const_12_5 (
    .out(const_12_5_out)
);
coreir_const #(
    .value(5'h0d),
    .width(5)
) const_13_5 (
    .out(const_13_5_out)
);
coreir_const #(
    .value(5'h0e),
    .width(5)
) const_14_5 (
    .out(const_14_5_out)
);
coreir_const #(
    .value(5'h0f),
    .width(5)
) const_15_5 (
    .out(const_15_5_out)
);
coreir_const #(
    .value(5'h10),
    .width(5)
) const_16_5 (
    .out(const_16_5_out)
);
coreir_const #(
    .value(5'h11),
    .width(5)
) const_17_5 (
    .out(const_17_5_out)
);
coreir_const #(
    .value(5'h01),
    .width(5)
) const_1_5 (
    .out(const_1_5_out)
);
coreir_const #(
    .value(5'h02),
    .width(5)
) const_2_5 (
    .out(const_2_5_out)
);
coreir_const #(
    .value(5'h03),
    .width(5)
) const_3_5 (
    .out(const_3_5_out)
);
coreir_const #(
    .value(5'h04),
    .width(5)
) const_4_5 (
    .out(const_4_5_out)
);
coreir_const #(
    .value(5'h05),
    .width(5)
) const_5_5 (
    .out(const_5_5_out)
);
coreir_const #(
    .value(5'h06),
    .width(5)
) const_6_5 (
    .out(const_6_5_out)
);
coreir_const #(
    .value(5'h07),
    .width(5)
) const_7_5 (
    .out(const_7_5_out)
);
coreir_const #(
    .value(5'h08),
    .width(5)
) const_8_5 (
    .out(const_8_5_out)
);
coreir_const #(
    .value(5'h09),
    .width(5)
) const_9_5 (
    .out(const_9_5_out)
);
corebit_and magma_Bit_and_inst0 (
    .in0(C),
    .in1(magma_Bit_not_inst4_out),
    .out(magma_Bit_and_inst0_out)
);
corebit_and magma_Bit_and_inst1 (
    .in0(magma_Bit_not_inst7_out),
    .in1(magma_Bit_not_inst8_out),
    .out(magma_Bit_and_inst1_out)
);
corebit_and magma_Bit_and_inst2 (
    .in0(magma_Bit_not_inst10_out),
    .in1(magma_Bit_not_inst11_out),
    .out(magma_Bit_and_inst2_out)
);
corebit_and magma_Bit_and_inst3 (
    .in0(N),
    .in1(magma_Bit_not_inst12_out),
    .out(magma_Bit_and_inst3_out)
);
corebit_not magma_Bit_not_inst0 (
    .in(Z),
    .out(magma_Bit_not_inst0_out)
);
corebit_not magma_Bit_not_inst1 (
    .in(C),
    .out(magma_Bit_not_inst1_out)
);
corebit_not magma_Bit_not_inst10 (
    .in(N),
    .out(magma_Bit_not_inst10_out)
);
corebit_not magma_Bit_not_inst11 (
    .in(Z),
    .out(magma_Bit_not_inst11_out)
);
corebit_not magma_Bit_not_inst12 (
    .in(Z),
    .out(magma_Bit_not_inst12_out)
);
corebit_not magma_Bit_not_inst2 (
    .in(N),
    .out(magma_Bit_not_inst2_out)
);
corebit_not magma_Bit_not_inst3 (
    .in(V),
    .out(magma_Bit_not_inst3_out)
);
corebit_not magma_Bit_not_inst4 (
    .in(Z),
    .out(magma_Bit_not_inst4_out)
);
corebit_not magma_Bit_not_inst5 (
    .in(C),
    .out(magma_Bit_not_inst5_out)
);
corebit_not magma_Bit_not_inst6 (
    .in(magma_Bit_xor_inst0_out),
    .out(magma_Bit_not_inst6_out)
);
corebit_not magma_Bit_not_inst7 (
    .in(Z),
    .out(magma_Bit_not_inst7_out)
);
corebit_not magma_Bit_not_inst8 (
    .in(magma_Bit_xor_inst2_out),
    .out(magma_Bit_not_inst8_out)
);
corebit_not magma_Bit_not_inst9 (
    .in(N),
    .out(magma_Bit_not_inst9_out)
);
corebit_or magma_Bit_or_inst0 (
    .in0(magma_Bit_not_inst5_out),
    .in1(Z),
    .out(magma_Bit_or_inst0_out)
);
corebit_or magma_Bit_or_inst1 (
    .in0(Z),
    .in1(magma_Bit_xor_inst3_out),
    .out(magma_Bit_or_inst1_out)
);
corebit_or magma_Bit_or_inst2 (
    .in0(magma_Bit_not_inst9_out),
    .in1(Z),
    .out(magma_Bit_or_inst2_out)
);
corebit_or magma_Bit_or_inst3 (
    .in0(N),
    .in1(Z),
    .out(magma_Bit_or_inst3_out)
);
corebit_or magma_Bit_or_inst4 (
    .in0(magma_Bits_5_eq_inst2_out),
    .in1(magma_Bits_5_eq_inst3_out),
    .out(magma_Bit_or_inst4_out)
);
corebit_or magma_Bit_or_inst5 (
    .in0(magma_Bits_5_eq_inst4_out),
    .in1(magma_Bits_5_eq_inst5_out),
    .out(magma_Bit_or_inst5_out)
);
corebit_xor magma_Bit_xor_inst0 (
    .in0(N),
    .in1(V),
    .out(magma_Bit_xor_inst0_out)
);
corebit_xor magma_Bit_xor_inst1 (
    .in0(N),
    .in1(V),
    .out(magma_Bit_xor_inst1_out)
);
corebit_xor magma_Bit_xor_inst2 (
    .in0(N),
    .in1(V),
    .out(magma_Bit_xor_inst2_out)
);
corebit_xor magma_Bit_xor_inst3 (
    .in0(N),
    .in1(V),
    .out(magma_Bit_xor_inst3_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst0 (
    .in0(code),
    .in1(const_0_5_out),
    .out(magma_Bits_5_eq_inst0_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst1 (
    .in0(code),
    .in1(const_1_5_out),
    .out(magma_Bits_5_eq_inst1_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst10 (
    .in0(code),
    .in1(const_8_5_out),
    .out(magma_Bits_5_eq_inst10_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst11 (
    .in0(code),
    .in1(const_9_5_out),
    .out(magma_Bits_5_eq_inst11_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst12 (
    .in0(code),
    .in1(const_10_5_out),
    .out(magma_Bits_5_eq_inst12_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst13 (
    .in0(code),
    .in1(const_11_5_out),
    .out(magma_Bits_5_eq_inst13_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst14 (
    .in0(code),
    .in1(const_12_5_out),
    .out(magma_Bits_5_eq_inst14_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst15 (
    .in0(code),
    .in1(const_13_5_out),
    .out(magma_Bits_5_eq_inst15_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst16 (
    .in0(code),
    .in1(const_14_5_out),
    .out(magma_Bits_5_eq_inst16_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst17 (
    .in0(code),
    .in1(const_15_5_out),
    .out(magma_Bits_5_eq_inst17_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst18 (
    .in0(code),
    .in1(const_16_5_out),
    .out(magma_Bits_5_eq_inst18_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst19 (
    .in0(code),
    .in1(const_17_5_out),
    .out(magma_Bits_5_eq_inst19_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst2 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst2_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst3 (
    .in0(code),
    .in1(const_2_5_out),
    .out(magma_Bits_5_eq_inst3_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst4 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst4_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst5 (
    .in0(code),
    .in1(const_3_5_out),
    .out(magma_Bits_5_eq_inst5_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst6 (
    .in0(code),
    .in1(const_4_5_out),
    .out(magma_Bits_5_eq_inst6_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst7 (
    .in0(code),
    .in1(const_5_5_out),
    .out(magma_Bits_5_eq_inst7_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst8 (
    .in0(code),
    .in1(const_6_5_out),
    .out(magma_Bits_5_eq_inst8_out)
);
coreir_eq #(
    .width(5)
) magma_Bits_5_eq_inst9 (
    .in0(code),
    .in1(const_7_5_out),
    .out(magma_Bits_5_eq_inst9_out)
);
assign O = Mux2xOutBit_inst17_O;
endmodule

module ALU (
    input [3:0] alu,
    input [0:0] signed_,
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
wire Mux2xBit_inst0_O;
wire Mux2xOutBit_inst0_O;
wire Mux2xOutBit_inst1_O;
wire Mux2xOutBit_inst10_O;
wire Mux2xOutBit_inst11_O;
wire Mux2xOutBit_inst12_O;
wire Mux2xOutBit_inst13_O;
wire Mux2xOutBit_inst14_O;
wire Mux2xOutBit_inst15_O;
wire Mux2xOutBit_inst16_O;
wire Mux2xOutBit_inst17_O;
wire Mux2xOutBit_inst18_O;
wire Mux2xOutBit_inst19_O;
wire Mux2xOutBit_inst2_O;
wire Mux2xOutBit_inst3_O;
wire Mux2xOutBit_inst4_O;
wire Mux2xOutBit_inst5_O;
wire Mux2xOutBit_inst6_O;
wire Mux2xOutBit_inst7_O;
wire Mux2xOutBit_inst8_O;
wire Mux2xOutBit_inst9_O;
wire [15:0] Mux2xOutUInt16_inst0_O;
wire [15:0] Mux2xOutUInt16_inst1_O;
wire [15:0] Mux2xOutUInt16_inst10_O;
wire [15:0] Mux2xOutUInt16_inst11_O;
wire [15:0] Mux2xOutUInt16_inst12_O;
wire [15:0] Mux2xOutUInt16_inst13_O;
wire [15:0] Mux2xOutUInt16_inst14_O;
wire [15:0] Mux2xOutUInt16_inst15_O;
wire [15:0] Mux2xOutUInt16_inst2_O;
wire [15:0] Mux2xOutUInt16_inst3_O;
wire [15:0] Mux2xOutUInt16_inst4_O;
wire [15:0] Mux2xOutUInt16_inst5_O;
wire [15:0] Mux2xOutUInt16_inst6_O;
wire [15:0] Mux2xOutUInt16_inst7_O;
wire [15:0] Mux2xOutUInt16_inst8_O;
wire [15:0] Mux2xOutUInt16_inst9_O;
wire bit_const_0_None_out;
wire bit_const_1_None_out;
wire [15:0] const_0_16_out;
wire [3:0] const_0_4_out;
wire [3:0] const_10_4_out;
wire [0:0] const_1_1_out;
wire [3:0] const_1_4_out;
wire [3:0] const_2_4_out;
wire [3:0] const_3_4_out;
wire [3:0] const_4_4_out;
wire [3:0] const_5_4_out;
wire [3:0] const_6_4_out;
wire [3:0] const_7_4_out;
wire [3:0] const_8_4_out;
wire [3:0] const_9_4_out;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst1_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst3_out;
wire magma_Bit_not_inst0_out;
wire magma_Bit_not_inst1_out;
wire magma_Bit_not_inst2_out;
wire magma_Bit_or_inst0_out;
wire magma_Bit_or_inst1_out;
wire magma_Bit_or_inst2_out;
wire magma_Bit_or_inst3_out;
wire magma_Bit_or_inst4_out;
wire magma_Bit_or_inst5_out;
wire magma_Bit_or_inst6_out;
wire [15:0] magma_Bits_16_and_inst0_out;
wire [15:0] magma_Bits_16_ashr_inst0_out;
wire magma_Bits_16_eq_inst0_out;
wire [15:0] magma_Bits_16_lshr_inst0_out;
wire [15:0] magma_Bits_16_neg_inst0_out;
wire [15:0] magma_Bits_16_neg_inst1_out;
wire [15:0] magma_Bits_16_not_inst0_out;
wire [15:0] magma_Bits_16_or_inst0_out;
wire magma_Bits_16_sge_inst0_out;
wire magma_Bits_16_sge_inst1_out;
wire [15:0] magma_Bits_16_shl_inst0_out;
wire magma_Bits_16_sle_inst0_out;
wire magma_Bits_16_slt_inst0_out;
wire magma_Bits_16_uge_inst0_out;
wire magma_Bits_16_uge_inst1_out;
wire magma_Bits_16_ule_inst0_out;
wire [15:0] magma_Bits_16_xor_inst0_out;
wire [16:0] magma_Bits_17_add_inst0_out;
wire [16:0] magma_Bits_17_add_inst1_out;
wire [16:0] magma_Bits_17_add_inst2_out;
wire [16:0] magma_Bits_17_add_inst3_out;
wire magma_Bits_1_eq_inst0_out;
wire magma_Bits_1_eq_inst1_out;
wire magma_Bits_1_eq_inst2_out;
wire magma_Bits_1_eq_inst3_out;
wire magma_Bits_4_eq_inst0_out;
wire magma_Bits_4_eq_inst1_out;
wire magma_Bits_4_eq_inst10_out;
wire magma_Bits_4_eq_inst11_out;
wire magma_Bits_4_eq_inst12_out;
wire magma_Bits_4_eq_inst13_out;
wire magma_Bits_4_eq_inst14_out;
wire magma_Bits_4_eq_inst15_out;
wire magma_Bits_4_eq_inst16_out;
wire magma_Bits_4_eq_inst17_out;
wire magma_Bits_4_eq_inst18_out;
wire magma_Bits_4_eq_inst19_out;
wire magma_Bits_4_eq_inst2_out;
wire magma_Bits_4_eq_inst20_out;
wire magma_Bits_4_eq_inst21_out;
wire magma_Bits_4_eq_inst22_out;
wire magma_Bits_4_eq_inst23_out;
wire magma_Bits_4_eq_inst24_out;
wire magma_Bits_4_eq_inst25_out;
wire magma_Bits_4_eq_inst26_out;
wire magma_Bits_4_eq_inst27_out;
wire magma_Bits_4_eq_inst28_out;
wire magma_Bits_4_eq_inst29_out;
wire magma_Bits_4_eq_inst3_out;
wire magma_Bits_4_eq_inst30_out;
wire magma_Bits_4_eq_inst31_out;
wire magma_Bits_4_eq_inst32_out;
wire magma_Bits_4_eq_inst33_out;
wire magma_Bits_4_eq_inst34_out;
wire magma_Bits_4_eq_inst4_out;
wire magma_Bits_4_eq_inst5_out;
wire magma_Bits_4_eq_inst6_out;
wire magma_Bits_4_eq_inst7_out;
wire magma_Bits_4_eq_inst8_out;
wire magma_Bits_4_eq_inst9_out;
Mux2xBit Mux2xBit_inst0 (
    .I0(Mux2xOutBit_inst11_O),
    .I1(a[15]),
    .S(magma_Bits_4_eq_inst20_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst0 (
    .I0(magma_Bits_16_uge_inst1_out),
    .I1(magma_Bits_16_sge_inst1_out),
    .S(magma_Bits_1_eq_inst0_out),
    .O(Mux2xOutBit_inst0_O)
);
Mux2xOutBit Mux2xOutBit_inst1 (
    .I0(magma_Bits_16_uge_inst0_out),
    .I1(magma_Bits_16_sge_inst0_out),
    .S(magma_Bits_1_eq_inst1_out),
    .O(Mux2xOutBit_inst1_O)
);
Mux2xOutBit Mux2xOutBit_inst10 (
    .I0(bit_const_0_None_out),
    .I1(magma_Bits_17_add_inst3_out[16]),
    .S(magma_Bits_4_eq_inst15_out),
    .O(Mux2xOutBit_inst10_O)
);
Mux2xOutBit Mux2xOutBit_inst11 (
    .I0(Mux2xOutBit_inst9_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst17_out),
    .O(Mux2xOutBit_inst11_O)
);
Mux2xOutBit Mux2xOutBit_inst12 (
    .I0(Mux2xOutBit_inst10_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst18_out),
    .O(Mux2xOutBit_inst12_O)
);
Mux2xOutBit Mux2xOutBit_inst13 (
    .I0(Mux2xOutBit_inst12_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst21_out),
    .O(Mux2xOutBit_inst13_O)
);
Mux2xOutBit Mux2xOutBit_inst14 (
    .I0(Mux2xBit_inst0_O),
    .I1(Mux2xOutBit_inst2_O),
    .S(magma_Bits_4_eq_inst23_out),
    .O(Mux2xOutBit_inst14_O)
);
Mux2xOutBit Mux2xOutBit_inst15 (
    .I0(Mux2xOutBit_inst13_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst24_out),
    .O(Mux2xOutBit_inst15_O)
);
Mux2xOutBit Mux2xOutBit_inst16 (
    .I0(Mux2xOutBit_inst14_O),
    .I1(Mux2xOutBit_inst1_O),
    .S(magma_Bits_4_eq_inst26_out),
    .O(Mux2xOutBit_inst16_O)
);
Mux2xOutBit Mux2xOutBit_inst17 (
    .I0(Mux2xOutBit_inst15_O),
    .I1(magma_Bits_17_add_inst1_out[16]),
    .S(magma_Bit_or_inst3_out),
    .O(Mux2xOutBit_inst17_O)
);
Mux2xOutBit Mux2xOutBit_inst18 (
    .I0(bit_const_0_None_out),
    .I1(magma_Bit_or_inst2_out),
    .S(magma_Bit_or_inst4_out),
    .O(Mux2xOutBit_inst18_O)
);
Mux2xOutBit Mux2xOutBit_inst19 (
    .I0(Mux2xOutBit_inst16_O),
    .I1(magma_Bits_17_add_inst1_out[16]),
    .S(magma_Bit_or_inst6_out),
    .O(Mux2xOutBit_inst19_O)
);
Mux2xOutBit Mux2xOutBit_inst2 (
    .I0(magma_Bits_16_ule_inst0_out),
    .I1(magma_Bits_16_sle_inst0_out),
    .S(magma_Bits_1_eq_inst2_out),
    .O(Mux2xOutBit_inst2_O)
);
Mux2xOutBit Mux2xOutBit_inst3 (
    .I0(bit_const_0_None_out),
    .I1(bit_const_1_None_out),
    .S(magma_Bit_or_inst1_out),
    .O(Mux2xOutBit_inst3_O)
);
Mux2xOutBit Mux2xOutBit_inst4 (
    .I0(Mux2xOutBit_inst3_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst4_out),
    .O(Mux2xOutBit_inst4_O)
);
Mux2xOutBit Mux2xOutBit_inst5 (
    .I0(bit_const_0_None_out),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst6_out),
    .O(Mux2xOutBit_inst5_O)
);
Mux2xOutBit Mux2xOutBit_inst6 (
    .I0(Mux2xOutBit_inst5_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst8_out),
    .O(Mux2xOutBit_inst6_O)
);
Mux2xOutBit Mux2xOutBit_inst7 (
    .I0(Mux2xOutBit_inst6_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst10_out),
    .O(Mux2xOutBit_inst7_O)
);
Mux2xOutBit Mux2xOutBit_inst8 (
    .I0(Mux2xOutBit_inst7_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst12_out),
    .O(Mux2xOutBit_inst8_O)
);
Mux2xOutBit Mux2xOutBit_inst9 (
    .I0(Mux2xOutBit_inst8_O),
    .I1(bit_const_0_None_out),
    .S(magma_Bits_4_eq_inst14_out),
    .O(Mux2xOutBit_inst9_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(magma_Bits_16_lshr_inst0_out),
    .I1(magma_Bits_16_ashr_inst0_out),
    .S(magma_Bits_1_eq_inst3_out),
    .O(Mux2xOutUInt16_inst0_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst1 (
    .I0(b),
    .I1(magma_Bits_16_not_inst0_out),
    .S(magma_Bit_or_inst0_out),
    .O(Mux2xOutUInt16_inst1_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst10 (
    .I0(Mux2xOutUInt16_inst9_O),
    .I1(magma_Bits_16_and_inst0_out),
    .S(magma_Bits_4_eq_inst13_out),
    .O(Mux2xOutUInt16_inst10_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst11 (
    .I0(Mux2xOutUInt16_inst10_O),
    .I1(Mux2xOutUInt16_inst5_O),
    .S(magma_Bits_4_eq_inst16_out),
    .O(Mux2xOutUInt16_inst11_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst12 (
    .I0(Mux2xOutUInt16_inst11_O),
    .I1(Mux2xOutUInt16_inst4_O),
    .S(magma_Bits_4_eq_inst19_out),
    .O(Mux2xOutUInt16_inst12_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst13 (
    .I0(Mux2xOutUInt16_inst12_O),
    .I1(Mux2xOutUInt16_inst3_O),
    .S(magma_Bits_4_eq_inst22_out),
    .O(Mux2xOutUInt16_inst13_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst14 (
    .I0(Mux2xOutUInt16_inst13_O),
    .I1(Mux2xOutUInt16_inst2_O),
    .S(magma_Bits_4_eq_inst25_out),
    .O(Mux2xOutUInt16_inst14_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst15 (
    .I0(Mux2xOutUInt16_inst14_O),
    .I1(magma_Bits_17_add_inst1_out[15:0]),
    .S(magma_Bit_or_inst5_out),
    .O(Mux2xOutUInt16_inst15_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst2 (
    .I0(Mux2xOutUInt16_inst1_O),
    .I1(a),
    .S(Mux2xOutBit_inst1_O),
    .O(Mux2xOutUInt16_inst2_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst3 (
    .I0(Mux2xOutUInt16_inst1_O),
    .I1(a),
    .S(Mux2xOutBit_inst2_O),
    .O(Mux2xOutUInt16_inst3_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst4 (
    .I0(magma_Bits_16_neg_inst0_out),
    .I1(a),
    .S(Mux2xOutBit_inst0_O),
    .O(Mux2xOutUInt16_inst4_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst5 (
    .I0(magma_Bits_17_add_inst3_out[15:0]),
    .I1(magma_Bits_16_neg_inst1_out),
    .S(magma_Bits_16_slt_inst0_out),
    .O(Mux2xOutUInt16_inst5_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst6 (
    .I0(const_0_16_out),
    .I1(magma_Bits_16_shl_inst0_out),
    .S(magma_Bits_4_eq_inst5_out),
    .O(Mux2xOutUInt16_inst6_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst7 (
    .I0(Mux2xOutUInt16_inst6_O),
    .I1(Mux2xOutUInt16_inst0_O),
    .S(magma_Bits_4_eq_inst7_out),
    .O(Mux2xOutUInt16_inst7_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst8 (
    .I0(Mux2xOutUInt16_inst7_O),
    .I1(magma_Bits_16_xor_inst0_out),
    .S(magma_Bits_4_eq_inst9_out),
    .O(Mux2xOutUInt16_inst8_O)
);
Mux2xOutUInt16 Mux2xOutUInt16_inst9 (
    .I0(Mux2xOutUInt16_inst8_O),
    .I1(magma_Bits_16_or_inst0_out),
    .S(magma_Bits_4_eq_inst11_out),
    .O(Mux2xOutUInt16_inst9_O)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
corebit_const #(
    .value(1'b1)
) bit_const_1_None (
    .out(bit_const_1_None_out)
);
coreir_const #(
    .value(16'h0000),
    .width(16)
) const_0_16 (
    .out(const_0_16_out)
);
coreir_const #(
    .value(4'h0),
    .width(4)
) const_0_4 (
    .out(const_0_4_out)
);
coreir_const #(
    .value(4'ha),
    .width(4)
) const_10_4 (
    .out(const_10_4_out)
);
coreir_const #(
    .value(1'h1),
    .width(1)
) const_1_1 (
    .out(const_1_1_out)
);
coreir_const #(
    .value(4'h1),
    .width(4)
) const_1_4 (
    .out(const_1_4_out)
);
coreir_const #(
    .value(4'h2),
    .width(4)
) const_2_4 (
    .out(const_2_4_out)
);
coreir_const #(
    .value(4'h3),
    .width(4)
) const_3_4 (
    .out(const_3_4_out)
);
coreir_const #(
    .value(4'h4),
    .width(4)
) const_4_4 (
    .out(const_4_4_out)
);
coreir_const #(
    .value(4'h5),
    .width(4)
) const_5_4 (
    .out(const_5_4_out)
);
coreir_const #(
    .value(4'h6),
    .width(4)
) const_6_4 (
    .out(const_6_4_out)
);
coreir_const #(
    .value(4'h7),
    .width(4)
) const_7_4 (
    .out(const_7_4_out)
);
coreir_const #(
    .value(4'h8),
    .width(4)
) const_8_4 (
    .out(const_8_4_out)
);
coreir_const #(
    .value(4'h9),
    .width(4)
) const_9_4 (
    .out(const_9_4_out)
);
corebit_and magma_Bit_and_inst0 (
    .in0(a[15]),
    .in1(Mux2xOutUInt16_inst1_O[15]),
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
    .in(Mux2xOutUInt16_inst1_O[15]),
    .out(magma_Bit_not_inst2_out)
);
corebit_or magma_Bit_or_inst0 (
    .in0(magma_Bits_4_eq_inst0_out),
    .in1(magma_Bits_4_eq_inst1_out),
    .out(magma_Bit_or_inst0_out)
);
corebit_or magma_Bit_or_inst1 (
    .in0(magma_Bits_4_eq_inst2_out),
    .in1(magma_Bits_4_eq_inst3_out),
    .out(magma_Bit_or_inst1_out)
);
corebit_or magma_Bit_or_inst2 (
    .in0(magma_Bit_and_inst1_out),
    .in1(magma_Bit_and_inst3_out),
    .out(magma_Bit_or_inst2_out)
);
corebit_or magma_Bit_or_inst3 (
    .in0(magma_Bits_4_eq_inst27_out),
    .in1(magma_Bits_4_eq_inst28_out),
    .out(magma_Bit_or_inst3_out)
);
corebit_or magma_Bit_or_inst4 (
    .in0(magma_Bits_4_eq_inst29_out),
    .in1(magma_Bits_4_eq_inst30_out),
    .out(magma_Bit_or_inst4_out)
);
corebit_or magma_Bit_or_inst5 (
    .in0(magma_Bits_4_eq_inst31_out),
    .in1(magma_Bits_4_eq_inst32_out),
    .out(magma_Bit_or_inst5_out)
);
corebit_or magma_Bit_or_inst6 (
    .in0(magma_Bits_4_eq_inst33_out),
    .in1(magma_Bits_4_eq_inst34_out),
    .out(magma_Bit_or_inst6_out)
);
coreir_and #(
    .width(16)
) magma_Bits_16_and_inst0 (
    .in0(a),
    .in1(Mux2xOutUInt16_inst1_O),
    .out(magma_Bits_16_and_inst0_out)
);
coreir_ashr #(
    .width(16)
) magma_Bits_16_ashr_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_ashr_inst0_out)
);
coreir_eq #(
    .width(16)
) magma_Bits_16_eq_inst0 (
    .in0(Mux2xOutUInt16_inst15_O),
    .in1(const_0_16_out),
    .out(magma_Bits_16_eq_inst0_out)
);
coreir_lshr #(
    .width(16)
) magma_Bits_16_lshr_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_lshr_inst0_out)
);
coreir_neg #(
    .width(16)
) magma_Bits_16_neg_inst0 (
    .in(a),
    .out(magma_Bits_16_neg_inst0_out)
);
coreir_neg #(
    .width(16)
) magma_Bits_16_neg_inst1 (
    .in(magma_Bits_17_add_inst3_out[15:0]),
    .out(magma_Bits_16_neg_inst1_out)
);
coreir_not #(
    .width(16)
) magma_Bits_16_not_inst0 (
    .in(b),
    .out(magma_Bits_16_not_inst0_out)
);
coreir_or #(
    .width(16)
) magma_Bits_16_or_inst0 (
    .in0(a),
    .in1(Mux2xOutUInt16_inst1_O),
    .out(magma_Bits_16_or_inst0_out)
);
coreir_sge #(
    .width(16)
) magma_Bits_16_sge_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_sge_inst0_out)
);
coreir_sge #(
    .width(16)
) magma_Bits_16_sge_inst1 (
    .in0(a),
    .in1(const_0_16_out),
    .out(magma_Bits_16_sge_inst1_out)
);
coreir_shl #(
    .width(16)
) magma_Bits_16_shl_inst0 (
    .in0(a),
    .in1(Mux2xOutUInt16_inst1_O),
    .out(magma_Bits_16_shl_inst0_out)
);
coreir_sle #(
    .width(16)
) magma_Bits_16_sle_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_sle_inst0_out)
);
coreir_slt #(
    .width(16)
) magma_Bits_16_slt_inst0 (
    .in0(magma_Bits_17_add_inst3_out[15:0]),
    .in1(const_0_16_out),
    .out(magma_Bits_16_slt_inst0_out)
);
coreir_uge #(
    .width(16)
) magma_Bits_16_uge_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_uge_inst0_out)
);
coreir_uge #(
    .width(16)
) magma_Bits_16_uge_inst1 (
    .in0(a),
    .in1(const_0_16_out),
    .out(magma_Bits_16_uge_inst1_out)
);
coreir_ule #(
    .width(16)
) magma_Bits_16_ule_inst0 (
    .in0(a),
    .in1(b),
    .out(magma_Bits_16_ule_inst0_out)
);
coreir_xor #(
    .width(16)
) magma_Bits_16_xor_inst0 (
    .in0(a),
    .in1(Mux2xOutUInt16_inst1_O),
    .out(magma_Bits_16_xor_inst0_out)
);
wire [16:0] magma_Bits_17_add_inst0_in0;
assign magma_Bits_17_add_inst0_in0 = {bit_const_0_None_out,a[15:0]};
wire [16:0] magma_Bits_17_add_inst0_in1;
assign magma_Bits_17_add_inst0_in1 = {bit_const_0_None_out,Mux2xOutUInt16_inst1_O[15:0]};
coreir_add #(
    .width(17)
) magma_Bits_17_add_inst0 (
    .in0(magma_Bits_17_add_inst0_in0),
    .in1(magma_Bits_17_add_inst0_in1),
    .out(magma_Bits_17_add_inst0_out)
);
wire [16:0] magma_Bits_17_add_inst1_in1;
assign magma_Bits_17_add_inst1_in1 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,Mux2xOutBit_inst4_O};
coreir_add #(
    .width(17)
) magma_Bits_17_add_inst1 (
    .in0(magma_Bits_17_add_inst0_out),
    .in1(magma_Bits_17_add_inst1_in1),
    .out(magma_Bits_17_add_inst1_out)
);
wire [16:0] magma_Bits_17_add_inst2_in0;
assign magma_Bits_17_add_inst2_in0 = {bit_const_0_None_out,a[15:0]};
wire [16:0] magma_Bits_17_add_inst2_in1;
assign magma_Bits_17_add_inst2_in1 = {bit_const_0_None_out,Mux2xOutUInt16_inst1_O[15:0]};
coreir_add #(
    .width(17)
) magma_Bits_17_add_inst2 (
    .in0(magma_Bits_17_add_inst2_in0),
    .in1(magma_Bits_17_add_inst2_in1),
    .out(magma_Bits_17_add_inst2_out)
);
wire [16:0] magma_Bits_17_add_inst3_in1;
assign magma_Bits_17_add_inst3_in1 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,Mux2xOutBit_inst4_O};
coreir_add #(
    .width(17)
) magma_Bits_17_add_inst3 (
    .in0(magma_Bits_17_add_inst2_out),
    .in1(magma_Bits_17_add_inst3_in1),
    .out(magma_Bits_17_add_inst3_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst0 (
    .in0(signed_),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst0_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst1 (
    .in0(signed_),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst1_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst2 (
    .in0(signed_),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst2_out)
);
coreir_eq #(
    .width(1)
) magma_Bits_1_eq_inst3 (
    .in0(signed_),
    .in1(const_1_1_out),
    .out(magma_Bits_1_eq_inst3_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst0 (
    .in0(alu),
    .in1(const_1_4_out),
    .out(magma_Bits_4_eq_inst0_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst1 (
    .in0(alu),
    .in1(const_10_4_out),
    .out(magma_Bits_4_eq_inst1_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst10 (
    .in0(alu),
    .in1(const_9_4_out),
    .out(magma_Bits_4_eq_inst10_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst11 (
    .in0(alu),
    .in1(const_7_4_out),
    .out(magma_Bits_4_eq_inst11_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst12 (
    .in0(alu),
    .in1(const_7_4_out),
    .out(magma_Bits_4_eq_inst12_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst13 (
    .in0(alu),
    .in1(const_8_4_out),
    .out(magma_Bits_4_eq_inst13_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst14 (
    .in0(alu),
    .in1(const_8_4_out),
    .out(magma_Bits_4_eq_inst14_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst15 (
    .in0(alu),
    .in1(const_10_4_out),
    .out(magma_Bits_4_eq_inst15_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst16 (
    .in0(alu),
    .in1(const_10_4_out),
    .out(magma_Bits_4_eq_inst16_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst17 (
    .in0(alu),
    .in1(const_10_4_out),
    .out(magma_Bits_4_eq_inst17_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst18 (
    .in0(alu),
    .in1(const_2_4_out),
    .out(magma_Bits_4_eq_inst18_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst19 (
    .in0(alu),
    .in1(const_2_4_out),
    .out(magma_Bits_4_eq_inst19_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst2 (
    .in0(alu),
    .in1(const_1_4_out),
    .out(magma_Bits_4_eq_inst2_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst20 (
    .in0(alu),
    .in1(const_2_4_out),
    .out(magma_Bits_4_eq_inst20_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst21 (
    .in0(alu),
    .in1(const_4_4_out),
    .out(magma_Bits_4_eq_inst21_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst22 (
    .in0(alu),
    .in1(const_4_4_out),
    .out(magma_Bits_4_eq_inst22_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst23 (
    .in0(alu),
    .in1(const_4_4_out),
    .out(magma_Bits_4_eq_inst23_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst24 (
    .in0(alu),
    .in1(const_3_4_out),
    .out(magma_Bits_4_eq_inst24_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst25 (
    .in0(alu),
    .in1(const_3_4_out),
    .out(magma_Bits_4_eq_inst25_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst26 (
    .in0(alu),
    .in1(const_3_4_out),
    .out(magma_Bits_4_eq_inst26_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst27 (
    .in0(alu),
    .in1(const_0_4_out),
    .out(magma_Bits_4_eq_inst27_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst28 (
    .in0(alu),
    .in1(const_1_4_out),
    .out(magma_Bits_4_eq_inst28_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst29 (
    .in0(alu),
    .in1(const_0_4_out),
    .out(magma_Bits_4_eq_inst29_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst3 (
    .in0(alu),
    .in1(const_10_4_out),
    .out(magma_Bits_4_eq_inst3_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst30 (
    .in0(alu),
    .in1(const_1_4_out),
    .out(magma_Bits_4_eq_inst30_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst31 (
    .in0(alu),
    .in1(const_0_4_out),
    .out(magma_Bits_4_eq_inst31_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst32 (
    .in0(alu),
    .in1(const_1_4_out),
    .out(magma_Bits_4_eq_inst32_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst33 (
    .in0(alu),
    .in1(const_0_4_out),
    .out(magma_Bits_4_eq_inst33_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst34 (
    .in0(alu),
    .in1(const_1_4_out),
    .out(magma_Bits_4_eq_inst34_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst4 (
    .in0(alu),
    .in1(const_0_4_out),
    .out(magma_Bits_4_eq_inst4_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst5 (
    .in0(alu),
    .in1(const_6_4_out),
    .out(magma_Bits_4_eq_inst5_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst6 (
    .in0(alu),
    .in1(const_6_4_out),
    .out(magma_Bits_4_eq_inst6_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst7 (
    .in0(alu),
    .in1(const_5_4_out),
    .out(magma_Bits_4_eq_inst7_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst8 (
    .in0(alu),
    .in1(const_5_4_out),
    .out(magma_Bits_4_eq_inst8_out)
);
coreir_eq #(
    .width(4)
) magma_Bits_4_eq_inst9 (
    .in0(alu),
    .in1(const_9_4_out),
    .out(magma_Bits_4_eq_inst9_out)
);
assign O0 = Mux2xOutUInt16_inst15_O;
assign O1 = Mux2xOutBit_inst19_O;
assign O2 = magma_Bits_16_eq_inst0_out;
assign O3 = Mux2xOutUInt16_inst15_O[15];
assign O4 = Mux2xOutBit_inst17_O;
assign O5 = Mux2xOutBit_inst18_O;
endmodule

module PE (
    input [9:0] inst,
    input [31:0] inputs,
    input clk_en,
    output [15:0] O,
    input CLK
);
wire [15:0] ALU_inst0_O0;
wire ALU_inst0_O1;
wire ALU_inst0_O2;
wire ALU_inst0_O3;
wire ALU_inst0_O4;
wire ALU_inst0_O5;
wire Cond_inst0_O;
ALU ALU_inst0 (
    .alu(inst[3:0]),
    .signed_(inst[9]),
    .a(inputs[15:0]),
    .b(inputs[31:16]),
    .O0(ALU_inst0_O0),
    .O1(ALU_inst0_O1),
    .O2(ALU_inst0_O2),
    .O3(ALU_inst0_O3),
    .O4(ALU_inst0_O4),
    .O5(ALU_inst0_O5),
    .CLK(CLK)
);
Cond Cond_inst0 (
    .code(inst[8:4]),
    .alu(ALU_inst0_O1),
    .Z(ALU_inst0_O2),
    .N(ALU_inst0_O3),
    .C(ALU_inst0_O4),
    .V(ALU_inst0_O5),
    .O(Cond_inst0_O),
    .CLK(CLK)
);
assign O = ALU_inst0_O0;
endmodule

