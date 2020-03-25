from dataclasses import dataclass
from .isa import inst_arch_closure
from hwtypes import BitVector, Bit
import magma as m
from .common import DATAWIDTH

def asm_arch_closure(arch):
    Inst_fc = inst_arch_closure(arch)
    Inst = Inst_fc(Bit.get_family())
    Data = BitVector[DATAWIDTH]
    LUT_t = Inst.lut
    Cond_t = Inst.cond

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
        
    Signed_t = Inst.signed



    def gen_inst(alu, mul, mux_in0, mux_in1, mux_reg, mux_out, signed=Signed_t.unsigned, lut=0, cond=Cond_t.Z):

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
