module coreir_lshr #(
    parameter width = 1
) (
    input [width-1:0] in0,
    input [width-1:0] in1,
    output [width-1:0] out
);
  assign out = in0 >> in1;
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

module LUT (
    input [7:0] lut,
    input bit0,
    input bit1,
    input bit2,
    output O,
    input CLK,
    input ASYNCRESET
);
wire bit_const_0_None_out;
wire [7:0] const_1_8_out;
wire [7:0] magma_Bits_8_and_inst0_out;
wire [7:0] magma_Bits_8_lshr_inst0_out;
corebit_const #(
    .value(1'b0)
) bit_const_0_None (
    .out(bit_const_0_None_out)
);
coreir_const #(
    .value(8'h01),
    .width(8)
) const_1_8 (
    .out(const_1_8_out)
);
coreir_and #(
    .width(8)
) magma_Bits_8_and_inst0 (
    .in0(magma_Bits_8_lshr_inst0_out),
    .in1(const_1_8_out),
    .out(magma_Bits_8_and_inst0_out)
);
wire [7:0] magma_Bits_8_lshr_inst0_in1;
assign magma_Bits_8_lshr_inst0_in1 = {bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit_const_0_None_out,bit2,bit1,bit0};
coreir_lshr #(
    .width(8)
) magma_Bits_8_lshr_inst0 (
    .in0(lut),
    .in1(magma_Bits_8_lshr_inst0_in1),
    .out(magma_Bits_8_lshr_inst0_out)
);
assign O = magma_Bits_8_and_inst0_out[0];
endmodule

module PE (
    input [7:0] inst,
    input [2:0] inputs,
    input clk_en,
    output [0:0] O,
    input CLK,
    input ASYNCRESET
);
wire LUT_inst0_O;
LUT LUT_inst0 (
    .lut(inst),
    .bit0(inputs[0]),
    .bit1(inputs[1]),
    .bit2(inputs[2]),
    .O(LUT_inst0_O),
    .CLK(CLK),
    .ASYNCRESET(ASYNCRESET)
);
assign O = LUT_inst0_O;
endmodule

