from .cond import Cond_t
from .lut import LUT_t_fc
from .alu import ALU_t, Signed_t
from .mul import MUL_t
from peak import Const, family_closure
from hwtypes import Tuple, Product
import magma as m
"""
https://github.com/StanfordAHA/CGRAGenerator/wiki/PE-Spec
"""
def inst_arch_closure(arch):
    @family_closure
    def Inst_fc(family):

        LUT_t, _ = LUT_t_fc(family)

        ALU_t_list_type = Tuple[(ALU_t for _ in range(arch.num_alu))]
        Cond_t_list_type = Tuple[(Cond_t for _ in range(arch.num_alu + arch.num_add))]
        MUL_t_list_type = Tuple[(MUL_t for _ in range(arch.num_mul))]
        mux_list_type_in0 = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.modules[i].in0))] for i in range(len(arch.modules)) if len(arch.modules[i].in0) > 1)]
        mux_list_type_in1 = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.modules[i].in1))] for i in range(len(arch.modules)) if len(arch.modules[i].in1) > 1)]
        mux_list_type_reg = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.regs[i].in_))] for i in range(len(arch.regs)) if len(arch.regs[i].in_) > 1)]
        mux_list_type_output = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.outputs[i]))] for i in range(arch.num_outputs) if len(arch.outputs[i]) > 1)]


        class Inst(Product):

            if arch.num_alu > 0:
                alu= ALU_t_list_type
            
            if arch.num_alu + arch.num_add > 0:
                cond= Cond_t_list_type        # Condition code (see cond.py)
                
            if arch.num_mul > 0:          # ALU operation
                mul= MUL_t_list_type

            if arch.num_mux_in0 > 0:
                mux_in0 = mux_list_type_in0

            if arch.num_mux_in1 > 0:
                mux_in1 = mux_list_type_in1

            if arch.num_reg_mux > 0:
                mux_reg = mux_list_type_reg

            if arch.num_output_mux > 0:
                mux_out = mux_list_type_output

            signed= Signed_t     # unsigned or signed
            lut= LUT_t          # LUT operation as a 3-bit LUT

        return Inst
    return Inst_fc
