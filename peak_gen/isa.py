from .cond import Cond_t
from .lut import LUT_t_fc
from peak import Const, family_closure
from hwtypes import Tuple, Product, Enum
import magma as m
"""
https://github.com/StanfordAHA/CGRAGenerator/wiki/PE-Spec
"""
class Signed_t(Enum):
    unsigned = 0
    signed = 1
    
class ALU_t(Enum):
    Add = 0
    Sub = 1
    Abs = 2
    GTE_Max = 3
    LTE_Min = 4
    SHR = 5
    SHL = 6
    Or = 7
    And = 8
    XOr = 9

class MUL_t(Enum):
    Mult0 = 0x0
    Mult1 = 0x1


def inst_arch_closure(arch):
    @family_closure
    def Inst_fc(family):
        Data = family.BitVector[arch.input_width]
        Bit = family.Bit

        LUT_t, _ = LUT_t_fc(family)

        ALU_t_list_type = Tuple[(ALU_t for _ in range(arch.num_alu))]
        Cond_t_list_type = Tuple[(Cond_t for _ in range(arch.num_alu + arch.num_add))]
        MUL_t_list_type = Tuple[(MUL_t for _ in range(arch.num_mul))]
        Const_data_list_type = Tuple[(Data for _ in range(arch.num_const_inputs))]
        Signed_list_type = Tuple[(Signed_t for _ in range(arch.num_alu + arch.num_mul))]
        mux_list_type_in0 = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.modules[i].in0))] for i in range(len(arch.modules)) if len(arch.modules[i].in0) > 1)]
        mux_list_type_in1 = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.modules[i].in1))] for i in range(len(arch.modules)) if len(arch.modules[i].in1) > 1)]
        mux_list_type_sel = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.modules[i].sel))] for i in range(len(arch.modules)) if len(arch.modules[i].sel) > 1)]
        mux_list_type_reg = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.regs[i].in_))] for i in range(len(arch.regs)) if len(arch.regs[i].in_) > 1)]
        mux_list_type_output = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.outputs[i]))] for i in range(arch.num_outputs) if len(arch.outputs[i]) > 1)]


        class Inst(Product):

            if arch.num_alu > 0:
                alu = ALU_t_list_type
            
            if arch.num_alu + arch.num_add > 0:
                cond = Cond_t_list_type  
                
            if arch.num_mul > 0:
                mul = MUL_t_list_type

            if arch.num_const_inputs > 0:
                const_data = Const_data_list_type

            if arch.num_mux_in0 > 0:
                mux_in0 = mux_list_type_in0

            if arch.num_mux_in1 > 0:
                mux_in1 = mux_list_type_in1

            if arch.num_mux_sel > 0:
                mux_sel = mux_list_type_sel

            if arch.num_reg_mux > 0:
                mux_reg = mux_list_type_reg

            if arch.num_output_mux > 0:
                mux_out = mux_list_type_output

            signed = Signed_list_type     # unsigned or signed
            lut = LUT_t          # LUT operation as a 3-bit LUT

            # bit0 = Bit           # RegD constant (1-bit)
            # bit1 = Bit           # RegE constant (1-bit)
            # bit2 = Bit           # RegF constant (1-bit)


        return Inst
    return Inst_fc
