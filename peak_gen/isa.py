from .cond import Cond_t
from .lut import LUT_t_fc
from peak import Const, family_closure
from hwtypes import Tuple, Product, Enum
import magma as m

class Signed_t(Enum):
    unsigned = Enum.Auto() 
    signed = Enum.Auto()
    
class ALU_t(Enum):
    Add = Enum.Auto()
    Sub = Enum.Auto()
    Abs = Enum.Auto()
    GTE_Max = Enum.Auto()
    LTE_Min = Enum.Auto()
    SHR = Enum.Auto()
    SHL = Enum.Auto()
    Or = Enum.Auto()
    And = Enum.Auto()
    XOr = Enum.Auto()
    Absd = Enum.Auto()

class BIT_ALU_t(Enum):
    Or = Enum.Auto()
    And = Enum.Auto()
    XOr = Enum.Auto()

class FP_ALU_t(Enum):
    FP_add = Enum.Auto()
    FP_sub = Enum.Auto()
    FP_cmp = Enum.Auto()
    FP_mult = Enum.Auto()
    FGetMant = Enum.Auto()
    FAddIExp = Enum.Auto()
    FSubExp = Enum.Auto()
    FCnvExp2F = Enum.Auto()
    FGetFInt = Enum.Auto()
    FGetFFrac = Enum.Auto()
    FCnvInt2F = Enum.Auto()

class MUL_t(Enum):
    Mult0 = 0
    datagate = 1
    Mult1 = 2


def inst_arch_closure(arch):
    @family_closure
    def Inst_fc(family):
        Data = family.BitVector[arch.input_width]
        Bit = family.Bit

        LUT_t, _ = LUT_t_fc(family)

        ALU_t_list_type = Tuple[(ALU_t for _ in range(arch.num_alu))]
        BIT_ALU_t_list_type = Tuple[(BIT_ALU_t for _ in range(arch.num_bit_alu))]
        FP_ALU_t_list_type = Tuple[(FP_ALU_t for _ in range(arch.num_fp_alu))]
        Cond_t_list_type = Tuple[(Cond_t for _ in range(arch.num_alu + arch.num_fp_alu + arch.num_sub + arch.num_gte + arch.num_lte))]
        MUL_t_list_type = Tuple[(MUL_t for _ in range(arch.num_mul))]
        Const_data_list_type = Tuple[(Bit if arch.const_inputs[i].width == 1 else Data for i in range(arch.num_const_inputs))]
        Signed_list_type = Tuple[(Signed_t for _ in range(arch.num_alu + arch.num_mul + arch.num_fp_alu + arch.num_gte + arch.num_lte + arch.num_shr))]
        LUT_list_type = Tuple[(LUT_t for _ in range(arch.num_lut))]
        mux_list_type_in0 = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.modules[i].in0))] for i in range(len(arch.modules)) if len(arch.modules[i].in0) > 1)]
        mux_list_type_in1 = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.modules[i].in1))] for i in range(len(arch.modules)) if len(arch.modules[i].in1) > 1)]
        mux_list_type_in2 = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.modules[i].in2))] for i in range(len(arch.modules)) if len(arch.modules[i].in2) > 1)]
        mux_list_type_reg = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.regs[i].in_))] for i in range(len(arch.regs)) if len(arch.regs[i].in_) > 1)]
        mux_list_type_output = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.outputs[i]))] for i in range(arch.num_outputs) if len(arch.outputs[i]) > 1)]
        mux_list_type_bit_output = Tuple[(family.BitVector[m.math.log2_ceil(len(arch.bit_outputs[i]))] for i in range(arch.num_bit_outputs) if len(arch.bit_outputs[i]) > 1)]


        class Inst(Product):

            at_least_one = False

            if arch.num_alu > 0:
                alu = ALU_t_list_type
                at_least_one = True

            if arch.num_bit_alu > 0:
                bit_alu = BIT_ALU_t_list_type
                at_least_one = True

            if arch.num_fp_alu > 0:
                fp_alu = FP_ALU_t_list_type
                at_least_one = True
            
            if arch.num_alu + arch.num_fp_alu + arch.num_sub + arch.num_gte + arch.num_lte > 0:
                cond = Cond_t_list_type  
                at_least_one = True
                
            if arch.num_mul > 0:
                mul = MUL_t_list_type
                at_least_one = True

            if arch.num_const_inputs > 0:
                const_data = Const_data_list_type
                at_least_one = True

            if arch.num_mux_in0 > 0:
                mux_in0 = mux_list_type_in0
                at_least_one = True

            if arch.num_mux_in1 > 0:
                mux_in1 = mux_list_type_in1
                at_least_one = True

            if arch.num_mux_in2 > 0:
                mux_in2 = mux_list_type_in2
                at_least_one = True

            if arch.num_reg_mux > 0:
                mux_reg = mux_list_type_reg
                at_least_one = True

            if arch.num_output_mux > 0:
                mux_out = mux_list_type_output
                at_least_one = True

            if arch.num_bit_output_mux > 0:
                mux_bit_out = mux_list_type_bit_output
                at_least_one = True

            if arch.num_alu + arch.num_mul + arch.num_fp_alu + arch.num_gte + arch.num_lte + arch.num_shr > 0:
                signed = Signed_list_type     # unsigned or signed
                at_least_one = True

            if arch.num_lut > 0:
                lut = LUT_list_type          # LUT operation as a 3-bit LUT
                at_least_one = True
            
            if not at_least_one:
                dummy = Bit

        return Inst
    return Inst_fc
