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

module coreir_mul #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 * in1;
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

module commonlib_muxn__N2__width32 (
    input [31:0] in_data [1:0],
    input [0:0] in_sel,
    output [31:0] out
);
wire [31:0] _join_out;
coreir_mux #(
    .width(32)
) _join (
    .in0(in_data[0]),
    .in1(in_data[1]),
    .sel(in_sel[0]),
    .out(_join_out)
);
assign out = _join_out;
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

module Mux2xOutUInt32 (
    input [31:0] I0,
    input [31:0] I1,
    input S,
    output [31:0] O
);
wire [31:0] coreir_commonlib_mux2x32_inst0_out;
wire [31:0] coreir_commonlib_mux2x32_inst0_in_data [1:0];
assign coreir_commonlib_mux2x32_inst0_in_data[1] = I1;
assign coreir_commonlib_mux2x32_inst0_in_data[0] = I0;
commonlib_muxn__N2__width32 coreir_commonlib_mux2x32_inst0 (
    .in_data(coreir_commonlib_mux2x32_inst0_in_data),
    .in_sel(S),
    .out(coreir_commonlib_mux2x32_inst0_out)
);
assign O = coreir_commonlib_mux2x32_inst0_out;
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

module MUL (
    input [0:0] instr,
    input [0:0] signed_,
    input [15:0] a,
    input [15:0] b,
    output [15:0] O,
    input CLK
);
wire [15:0] Mux2xOutUInt16_inst0_O;
wire [31:0] Mux2xOutUInt32_inst0_O;
wire [31:0] Mux2xOutUInt32_inst1_O;
wire bit_const_0_None_out;
wire [0:0] const_0_1_out;
wire [0:0] const_1_1_out;
wire magma_Bits_1_eq_inst0_out;
wire magma_Bits_1_eq_inst1_out;
wire magma_Bits_1_eq_inst2_out;
wire [31:0] magma_Bits_32_mul_inst0_out;
Mux2xOutUInt16 Mux2xOutUInt16_inst0 (
    .I0(magma_Bits_32_mul_inst0_out[31:16]),
    .I1(magma_Bits_32_mul_inst0_out[15:0]),
    .S(magma_Bits_1_eq_inst2_out),
    .O(Mux2xOutUInt16_inst0_O)
);
wire [31:0] Mux2xOutUInt32_inst0_I0;
assign Mux2xOutUInt32_inst0_I0 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,a[15:0]};
wire [31:0] Mux2xOutUInt32_inst0_I1;
assign Mux2xOutUInt32_inst0_I1 = {a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15],a[15:0]};
Mux2xOutUInt32 Mux2xOutUInt32_inst0 (
    .I0(Mux2xOutUInt32_inst0_I0),
    .I1(Mux2xOutUInt32_inst0_I1),
    .S(magma_Bits_1_eq_inst0_out),
    .O(Mux2xOutUInt32_inst0_O)
);
wire [31:0] Mux2xOutUInt32_inst1_I0;
assign Mux2xOutUInt32_inst1_I0 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,b[15:0]};
wire [31:0] Mux2xOutUInt32_inst1_I1;
assign Mux2xOutUInt32_inst1_I1 = {b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15],b[15:0]};
Mux2xOutUInt32 Mux2xOutUInt32_inst1 (
    .I0(Mux2xOutUInt32_inst1_I0),
    .I1(Mux2xOutUInt32_inst1_I1),
    .S(magma_Bits_1_eq_inst1_out),
    .O(Mux2xOutUInt32_inst1_O)
);
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(1'h0),
    .width(1)
) const_0_1 (
    .out(const_0_1_out)
);
coreir_const #(
    .value(1'h1),
    .width(1)
) const_1_1 (
    .out(const_1_1_out)
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
    .in0(instr),
    .in1(const_0_1_out),
    .out(magma_Bits_1_eq_inst2_out)
);
coreir_mul #(
    .width(32)
) magma_Bits_32_mul_inst0 (
    .in0(Mux2xOutUInt32_inst0_O),
    .in1(Mux2xOutUInt32_inst1_O),
    .out(magma_Bits_32_mul_inst0_out)
);
assign O = Mux2xOutUInt16_inst0_O;
endmodule

module PE (
    input [1:0] inst,
    input [31:0] inputs,
    input clk_en,
    output [15:0] O,
    input CLK
);
wire [15:0] MUL_inst0_O;
MUL MUL_inst0 (
    .instr(inst[0]),
    .signed_(inst[1]),
    .a(inputs[15:0]),
    .b(inputs[31:16]),
    .O(MUL_inst0_O),
    .CLK(CLK)
);
assign O = MUL_inst0_O;
endmodule

