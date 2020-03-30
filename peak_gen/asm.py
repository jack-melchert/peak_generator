from dataclasses import dataclass
from .isa import inst_arch_closure
from .alu import ALU_t_fc
from .mul import MUL_t_fc
from .cond import Cond_t_fc
from hwtypes import BitVector, Bit
import magma as m

#Lut Constants
B0 = BitVector[8]([0,1,0,1,0,1,0,1])
B1 = BitVector[8]([0,0,1,1,0,0,1,1])
B2 = BitVector[8]([0,0,0,0,1,1,1,1])

def asm_arch_closure(arch):
    Inst_fc = inst_arch_closure(arch)
    Inst = Inst_fc(Bit.get_family())
    Data = BitVector[arch.input_width]
    LUT_t = Inst.lut
    Cond_t = Inst.cond
    ALU_t, _ = ALU_t_fc(Bit.get_family())
    MUL_t, _ = MUL_t_fc(Bit.get_family())

    if arch.num_alu > 0:
        ALU_t_list_type = Inst.alu

    if arch.num_mul > 0:
        MUL_t_list_type = Inst.mul
    
    if arch.num_mux_in0 > 0:
        mux_list_type_in0 = Inst.mux_in0

    if arch.num_mux_in1 > 0:
        mux_list_type_in1 = Inst.mux_in1

    if arch.num_reg_mux > 0:
        mux_list_type_reg = Inst.mux_reg


    if arch.num_output_mux > 0:
        mux_list_type_output = Inst.mux_out

    ALU_default = [ALU_t.Add for _ in range(arch.num_alu)]
    MUL_default = [MUL_t.Mult0 for _ in range(arch.num_mul)]
    mux_in0_default = [0 for _ in range(arch.num_mux_in0)]
    mux_in1_default = [0 for _ in range(arch.num_mux_in1)]
    mux_reg_default = [0 for _ in range(arch.num_reg_mux)]
    mux_out_default = [0 for _ in range(arch.num_output_mux)]
    Signed_t = Inst.signed



    def gen_inst(alu = ALU_default, mul = MUL_default, mux_in0 = mux_in0_default, \
    mux_in1 = mux_in1_default, mux_reg = mux_reg_default, mux_out = mux_out_default, \
    signed=Signed_t.unsigned, lut=0, cond=Cond_t.Z):

        args = []

        if arch.num_alu > 0:
            args.append(ALU_t_list_type(*alu))

        if arch.num_mul > 0:
            args.append(MUL_t_list_type(*mul) )

        if arch.num_mux_in0 > 0:
            args.append(mux_list_type_in0(*mux_in0) )

        if arch.num_mux_in1 > 0:
            args.append(mux_list_type_in1(*mux_in1) )

        if arch.num_reg_mux > 0:
            args.append(mux_list_type_reg(*mux_reg) )

        if arch.num_output_mux > 0:
            args.append(mux_list_type_output(*mux_out) )


        args.append(signed )
        args.append(LUT_t(lut) )
        args.append(cond)


        return Inst(*args)

    return gen_inst

def lut(arch, val):
    Cond_t = Cond_t_fc(Bit.get_family())
    return asm_arch_closure(arch)(lut=val,cond=Cond_t.LUT)

#Using bit1 and bit2 since bit0 can be used in the ALU
def lut_and(arch):
    return lut(arch, B1&B2)

def lut_or(arch):
    return lut(arch, B1|B2)

def lut_xor(arch):
    return lut(arch, B1^B2)

def lut_not(arch):
    return lut(arch, ~B1)

def lut_mux(arch):
    return lut(arch, (B2&B1)|((~B2)&B0))