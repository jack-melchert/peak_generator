from dataclasses import dataclass
from .isa import inst_arch_closure
from .isa import ALU_t
from .isa import BIT_ALU_t
from .isa import FP_ALU_t
from .isa import MUL_t
from .isa import Signed_t
from .cond import Cond_t
import magma as m
from peak import family, family_closure
from peak.family import AbstractFamily


def asm_arch_closure(arch):
    @family_closure
    def asm_fc(family : AbstractFamily):

        Inst_fc = inst_arch_closure(arch)
        Inst = Inst_fc(family)
        Data = family.BitVector[arch.input_width]
        Bit = family.Bit

        if hasattr(Inst, 'alu'):
            ALU_t_list_type = Inst.alu

        if hasattr(Inst, 'bit_alu'):
            BIT_ALU_t_list_type = Inst.bit_alu

        if hasattr(Inst, 'fp_alu'):
            FP_ALU_t_list_type = Inst.fp_alu

        if hasattr(Inst, 'cond'):
            Cond_t_list_type = Inst.cond

        if hasattr(Inst, 'mul'):
            MUL_t_list_type = Inst.mul

        if hasattr(Inst, 'const_data'):
            Const_data_t = Inst.const_data
        
        if hasattr(Inst, 'mux_in0'):
            mux_list_type_in0 = Inst.mux_in0

        if hasattr(Inst, 'mux_in1'):
            mux_list_type_in1 = Inst.mux_in1

        if hasattr(Inst, 'mux_in2'):
            mux_list_type_in2 = Inst.mux_in2

        if hasattr(Inst, 'mux_reg'):
            mux_list_type_reg = Inst.mux_reg

        if hasattr(Inst, 'mux_out'):
            mux_list_type_output = Inst.mux_out

        if hasattr(Inst, 'mux_bit_out'):
            mux_list_type_bit_output = Inst.mux_bit_out

        if hasattr(Inst, 'lut'):
            LUT_t_list_type = Inst.lut

        if hasattr(Inst, 'signed'):
            Signed_list_type = Inst.signed


        ALU_default = [ALU_t.Add for _ in range(arch.num_alu)]
        BIT_ALU_default = [BIT_ALU_t.And for _ in range(arch.num_bit_alu)]
        FP_ALU_default = [FP_ALU_t.FP_add for _ in range(arch.num_fp_alu)]
        Cond_default = [Cond_t.Z for _ in range(arch.num_alu + arch.num_add)]
        MUL_default = [MUL_t.Mult0 for _ in range(arch.num_mul)]
        Const_default = [Bit(0) if arch.const_inputs[i].width == 1 else Data(0) for i in range(arch.num_const_inputs)]
        LUT_default = [family.BitVector[8](0) for _ in range(arch.num_lut)]
        signed_default = [Signed_t.unsigned for _ in range(arch.num_alu + arch.num_fp_alu + arch.num_mul)]

        mux_in0_default = [family.BitVector[m.math.log2_ceil(len(arch.modules[i].in0))](0) for i in range(len(arch.modules)) if len(arch.modules[i].in0) > 1]
        mux_in1_default = [family.BitVector[m.math.log2_ceil(len(arch.modules[i].in1))](0) for i in range(len(arch.modules)) if len(arch.modules[i].in1) > 1]
        mux_in2_default = [family.BitVector[m.math.log2_ceil(len(arch.modules[i].in2))](0) for i in range(len(arch.modules)) if len(arch.modules[i].in2) > 1]
        mux_reg_default = [family.BitVector[m.math.log2_ceil(len(arch.regs[i].in_))](0) for i in range(len(arch.regs)) if len(arch.regs[i].in_) > 1]
        mux_out_default = [family.BitVector[m.math.log2_ceil(len(arch.outputs[i]))](0) for i in range(arch.num_outputs) if len(arch.outputs[i]) > 1]
        mux_bit_out_default = [family.BitVector[m.math.log2_ceil(len(arch.bit_outputs[i]))](0) for i in range(arch.num_bit_outputs) if len(arch.bit_outputs[i]) > 1]

        def gen_inst(alu = ALU_default, bit_alu = BIT_ALU_default, fp_alu=FP_ALU_default, cond=Cond_default, mul = MUL_default, const = Const_default, mux_in0 = mux_in0_default, \
        mux_in1 = mux_in1_default, mux_in2 = mux_in2_default, mux_reg = mux_reg_default, mux_out = mux_out_default, mux_bit_out = mux_bit_out_default,\
        signed=signed_default, lut=LUT_default):

            args = []

            if hasattr(Inst, 'alu'):
                args.append(ALU_t_list_type(*alu))

            if hasattr(Inst, 'bit_alu'):
                args.append(BIT_ALU_t_list_type(*bit_alu))

            if hasattr(Inst, 'fp_alu'):
                args.append(FP_ALU_t_list_type(*fp_alu))

            if hasattr(Inst, 'cond'):
                args.append(Cond_t_list_type(*cond))

            if hasattr(Inst, 'mul'):
                args.append(MUL_t_list_type(*mul) )

            if hasattr(Inst, 'const_data'):
                args.append(Const_data_t(*const))

            if hasattr(Inst, 'mux_in0'):
                args.append(mux_list_type_in0(*mux_in0) )

            if hasattr(Inst, 'mux_in1'):
                args.append(mux_list_type_in1(*mux_in1) )

            if hasattr(Inst, 'mux_in2'):
                args.append(mux_list_type_in2(*mux_in2) )

            if hasattr(Inst, 'mux_reg'):
                args.append(mux_list_type_reg(*mux_reg) )

            if hasattr(Inst, 'mux_out'):
                args.append(mux_list_type_output(*mux_out) )

            if hasattr(Inst, 'mux_bit_out'):
                args.append(mux_list_type_bit_output(*mux_bit_out) )

            if hasattr(Inst, 'signed'):
                args.append(Signed_list_type(*signed))

            if hasattr(Inst, 'lut'):
                args.append(LUT_t_list_type(*lut))

            if hasattr(Inst, 'dummy'):
                args.append(Bit(0))

            return Inst(*args)

        return gen_inst
    return asm_fc

