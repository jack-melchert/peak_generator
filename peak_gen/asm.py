from dataclasses import dataclass
from .isa import inst_arch_closure
from .isa import ALU_t
from .isa import MUL_t
from .isa import Signed_t
from .cond import Cond_t
import magma as m
from peak import family, family_closure
from peak.family import AbstractFamily

#Lut Constants

# B0 = family.PyFamily().BitVector[8]([0,1,0,1,0,1,0,1])
# B1 = family.PyFamily().BitVector[8]([0,0,1,1,0,0,1,1])
# B2 = family.PyFamily().BitVector[8]([0,0,0,0,1,1,1,1])

def asm_arch_closure(arch):
    @family_closure
    def asm_fc(family : AbstractFamily):

        Inst_fc = inst_arch_closure(arch)
        Inst = Inst_fc(family)
        Data = family.BitVector[arch.input_width]

        if arch.num_alu > 0:
            ALU_t_list_type = Inst.alu

        if arch.num_fp_alu > 0:
            FP_ALU_t_list_type = Inst.fp_alu

        if arch.num_alu + arch.num_add + arch.num_fp_alu > 0:
            Cond_t_list_type = Inst.cond

        if arch.num_mul > 0:
            MUL_t_list_type = Inst.mul

        if arch.num_const_inputs > 0:
            Const_data_t = Inst.const_data
        
        if arch.num_mux_in0 > 0:
            mux_list_type_in0 = Inst.mux_in0

        if arch.num_mux_in1 > 0:
            mux_list_type_in1 = Inst.mux_in1

        if arch.num_reg_mux > 0:
            mux_list_type_reg = Inst.mux_reg

        if arch.num_output_mux > 0:
            mux_list_type_output = Inst.mux_out

        if arch.num_lut > 0:
            LUT_t_list_type = Inst.lut

        if arch.num_alu + arch.num_mul + arch.num_fp_alu:
            Signed_list_type = Inst.signed

        ALU_default = [ALU_t.Add for _ in range(arch.num_alu)]
        FP_ALU_default = [FP_ALU_t.FP_add for _ in range(arch.num_fp_alu)]
        Cond_default = [Cond_t.Z for _ in range(arch.num_alu + arch.num_add)]
        MUL_default = [MUL_t.Mult0 for _ in range(arch.num_mul)]
        Const_default = [Data(0) for _ in range(arch.num_const_inputs)]
        LUT_default = [family.BitVector[8](0) for _ in range(arch.num_lut)]
        mux_in0_default = [family.BitVector[1](0) for _ in range(arch.num_mux_in0)]
        mux_in1_default = [family.BitVector[1](0) for _ in range(arch.num_mux_in1)]
        mux_reg_default = [family.BitVector[1](0) for _ in range(arch.num_reg_mux)]
        mux_out_default = [family.BitVector[1](0) for _ in range(arch.num_output_mux)]
        signed_default = [Signed_t.unsigned for _ in range(arch.num_alu + arch.num_fp_alu + arch.num_mul)]


        def gen_inst(alu = ALU_default, fp_alu=FP_ALU_default, cond=Cond_default, mul = MUL_default, const = Const_default, mux_in0 = mux_in0_default, \
        mux_in1 = mux_in1_default, mux_reg = mux_reg_default, mux_out = mux_out_default, \
        signed=signed_default, lut=LUT_default):

            args = []

            if arch.num_alu > 0:
                args.append(ALU_t_list_type(*alu))

            if arch.num_fp_alu > 0:
                args.append(FP_ALU_t_list_type(*fp_alu))

            if arch.num_alu + arch.num_add > 0:
                args.append(Cond_t_list_type(*cond))

            if arch.num_mul > 0:
                args.append(MUL_t_list_type(*mul) )

            if arch.num_const_inputs > 0:
                args.append(Const_data_t(*const))

            if arch.num_mux_in0 > 0:
                args.append(mux_list_type_in0(*mux_in0) )

            if arch.num_mux_in1 > 0:
                args.append(mux_list_type_in1(*mux_in1) )

            if arch.num_reg_mux > 0:
                args.append(mux_list_type_reg(*mux_reg) )

            if arch.num_output_mux > 0:
                args.append(mux_list_type_output(*mux_out) )

            if arch.num_alu + arch.num_mul + arch.num_fp_alu:
                args.append(Signed_list_type(*signed))

            if arch.num_lut > 0:
                args.append(LUT_t_list_type(*lut))


            return Inst(*args)

        return gen_inst
    return asm_fc

# def lut(arch, val):
#     Cond_default = [Cond_t.LUT for _ in range(arch.num_alu + arch.num_add)]
#     return asm_arch_closure(arch)(family.PyFamily())(lut=val, cond=Cond_default)

# #Using bit1 and bit2 since bit0 can be used in the ALU
# def lut_and(arch):
#     return lut(arch, B1&B2)

# def lut_or(arch):
#     return lut(arch, B1|B2)

# def lut_xor(arch):
#     return lut(arch, B1^B2)

# def lut_not(arch):
#     return lut(arch, ~B1)

# def lut_mux(arch):
#     return lut(arch, (B2&B1)|((~B2)&B0))