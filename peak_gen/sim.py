from peak import Peak, family_closure, name_outputs, gen_register, Const
from hwtypes.adt import Tuple, Product
from functools import lru_cache
import magma as m
import hwtypes
import ast_tools
from ast_tools.passes import apply_passes, if_inline, loop_unroll
from ast_tools.macros import inline, unroll
import inspect
from .common import *
from .lut import LUT_fc
from .alu import ALU_fc
from .bitwise_alu import BIT_ALU_fc
from .fp_alu import FP_ALU_fc, fp_unit_fc
from .add import ADD_fc
from .sub import SUB_fc
from .abs import ABS_fc
from .gte import GTE_fc
from .lte import LTE_fc
from .shr import SHR_fc
from .shl import SHL_fc
from .absd import ABSD_fc

from .cond import Cond_fc
from .isa import inst_arch_closure
from .arch import *
from .mul import MUL_fc
from .mux import MUX_fc
from peak.assembler import Assembler, AssembledADT
from peak.family import AbstractFamily
import peak 

def pe_arch_closure(arch):
    @family_closure
    def PE_fc(family: AbstractFamily):

        BitVector = family.BitVector
        Data = family.BitVector[arch.input_width]
        Out_Data = family.BitVector[arch.output_width]

        Bit = family.Bit
        Register = gen_register(Data, 0)(family)
        Bit_Register = gen_register(Bit, 0)(family)

        ALU_bw = ALU_fc(family)
        BIT_ALU_bw = BIT_ALU_fc(family)

        FP_ALU_bw = FP_ALU_fc(family)
        fp_unit_bw = fp_unit_fc(family)

        ADD_bw = ADD_fc(family)
        SUB_bw = SUB_fc(family)
        ABS_bw = ABS_fc(family)
        GTE_bw = GTE_fc(family)
        LTE_bw = LTE_fc(family)
        SHR_bw = SHR_fc(family)
        SHL_bw = SHL_fc(family)
        ABSD_bw = ABSD_fc(family)

        LUT = LUT_fc(family)
        MUL_bw = MUL_fc(family)
        MUX_bw = MUX_fc(family)
        Inst_fc = inst_arch_closure(arch)
        Inst = Inst_fc(family)
        Cond = Cond_fc(family)

        modules_type = []
        modules = []
        cond_type = []
        conds = []

        for module in arch.modules:
            if module.type_ == 'alu':
                modules_type.append(type(ALU_bw(module.in_width)))
                modules.append(ALU_bw(module.in_width))
                cond_type.append(Cond)
                conds.append(Cond)
            if module.type_ == 'bit_alu':
                modules_type.append(type(BIT_ALU_bw(module.in_width)))
                modules.append(BIT_ALU_bw(module.in_width))
            if module.type_ == 'fp_alu':
                modules_type.append(type(FP_ALU_bw(module.in_width)))
                modules.append(FP_ALU_bw(module.in_width))
                cond_type.append(Cond)
                conds.append(Cond)
            if module.type_ == 'mul':
                modules_type.append(type(MUL_bw(module.in_width, module.out_width)))
                modules.append(MUL_bw(module.in_width, module.out_width))
            if module.type_ == 'add':
                modules_type.append(type(ADD_bw(arch.input_width)))
                modules.append(ADD_bw(arch.input_width))
            if module.type_ == 'sub':
                modules_type.append(type(SUB_bw(arch.input_width)))
                modules.append(SUB_bw(arch.input_width))
                cond_type.append(Cond)
                conds.append(Cond)
            if module.type_ == 'abs':
                modules_type.append(type(ABS_bw(arch.input_width)))
                modules.append(ABS_bw(arch.input_width))
            if module.type_ == 'gte':
                modules_type.append(type(GTE_bw(arch.input_width)))
                modules.append(GTE_bw(arch.input_width))
                cond_type.append(Cond)
                conds.append(Cond)
            if module.type_ == 'lte':
                modules_type.append(type(LTE_bw(arch.input_width)))
                modules.append(LTE_bw(arch.input_width))
                cond_type.append(Cond)
                conds.append(Cond)
            if module.type_ == 'shr':
                modules_type.append(type(SHR_bw(arch.input_width)))
                modules.append(SHR_bw(arch.input_width))
            if module.type_ == 'shl':
                modules_type.append(type(SHL_bw(arch.input_width)))
                modules.append(SHL_bw(arch.input_width))
            if module.type_ == 'absd':
                modules_type.append(type(ABSD_bw(arch.input_width)))
                modules.append(ABSD_bw(arch.input_width))
            if module.type_ == 'mux':
                modules_type.append(type(MUX_bw(arch.input_width)))
                modules.append(MUX_bw(arch.input_width))
            if module.type_ == 'lut':
                modules_type.append(LUT)
                modules.append(LUT)


        DataInputList = Tuple[(Data if i < arch.num_inputs else Bit for i in range(arch.num_inputs + arch.num_bit_inputs))]

        Output_T = Tuple[(Out_Data if i < arch.num_outputs else Bit for i in range(arch.num_outputs + arch.num_bit_outputs))]
        Output_Tc = family.get_constructor(Output_T)

        class fp_val(Product):
            res = Data
            res_p = Bit
            Z = Bit
            N = Bit
            C = Bit
            V = Bit  

        @family.assemble(locals(), globals())
        class PE_gen(Peak, typecheck=True):
            @apply_passes([loop_unroll(), if_inline()])
            def __init__(self):

                # Data registers
                if inline(arch.enable_input_regs):
                    self.input_regs: [Register for _ in range(arch.num_inputs)] = [Register() for _ in range(arch.num_inputs)]
                    self.bit_input_regs: [Bit_Register for _ in range(arch.num_bit_inputs)] = [Bit_Register() for _ in range(arch.num_bit_inputs)]

                if inline(arch.enable_output_regs):
                    self.output_regs: [Register for _ in range(arch.num_outputs)] = [Register() for _ in range(arch.num_outputs)]
                    self.bit_output_regs: [Bit_Register for _ in range(arch.num_bit_outputs)] = [Bit_Register() for _ in range(arch.num_bit_outputs)]

                self.regs: [Register for _ in range(arch.num_reg)] = [Register() for _ in range(arch.num_reg)]

                self.bit_regs: [Register for _ in range(arch.num_bit_reg)] = [Bit_Register() for _ in range(arch.num_bit_reg)]

                self.modules: modules_type = [mod() for mod in modules]
                self.cond: cond_type = [cond() for cond in conds]

            @apply_passes([loop_unroll(), loop_unroll(), if_inline()])
            @name_outputs(pe_outputs=Output_T)
            def __call__(self, inst: Const(Inst), \
                               inputs: DataInputList, \
                               clk_en: Global(Bit) = Bit(1)) -> (Output_T):

                signals = {}
                bit_signals = {}

                #  Inputs with or without registers
                input_idx = 0
                if inline(arch.enable_input_regs):
                    for input_reg_idx in unroll(range(arch.num_inputs)):
                        signals[arch.inputs[input_reg_idx]] = self.input_regs[input_reg_idx](inputs[input_idx], clk_en)
                        input_idx = input_idx + 1
                    for symbol_interpolate in unroll(range(arch.num_bit_inputs)):
                        bit_signals[arch.bit_inputs[symbol_interpolate]] = self.bit_input_regs[symbol_interpolate](inputs[input_idx], clk_en)
                        input_idx = input_idx + 1
                        
                else:
                    for i in unroll(range(arch.num_inputs)):
                        signals[arch.inputs[input_idx]] = inputs[input_idx]
                        input_idx = input_idx + 1
                    for i in unroll(range(arch.num_bit_inputs)):
                        bit_signals[arch.bit_inputs[i]] = inputs[input_idx]
                        input_idx = input_idx + 1
                        
                # Constant inputs
                for i in unroll(range(arch.num_const_inputs)):
                    if inline(arch.const_inputs[i].width == 1):
                        bit_signals[arch.const_inputs[i].id] = inst.const_data[i]
                    else:
                        signals[arch.const_inputs[i].id] = inst.const_data[i]

                # Pipelining registers
                for symbol_interpolate in unroll(range(arch.num_reg)):
                    signals[arch.regs[symbol_interpolate].id] = self.regs[symbol_interpolate](Data(0), Bit(0))

                for symbol_interpolate in unroll(range(arch.num_bit_reg)):
                    bit_signals[arch.bit_regs[symbol_interpolate].id] = self.bit_regs[symbol_interpolate](Bit(0), Bit(0))

   
                mux_idx_in0 = 0
                mux_idx_in1 = 0
                mux_idx_in2 = 0
                signed_idx = 0
                mul_idx = 0
                alu_idx = 0
                bit_alu_idx = 0
                fp_alu_idx = 0
                lut_idx = 0
                cond_idx = 0
                Z = Bit(0)
                N = Bit(0)
                C = Bit(0)
                V = Bit(0)

                # Loop over modules (ALU, MUL, Adders, etc.)
                for symbol_interpolate in unroll(range(len(arch.modules))):
                    if inline(arch.modules[symbol_interpolate].type_ == "lut"):
                        if inline(len(arch.modules[symbol_interpolate].in0) == 1):
                            in0 = bit_signals[arch.modules[symbol_interpolate].in0[0]]  
                        else:
                            in0_mux_select = inst.mux_in0[mux_idx_in0]
                            in0 = bit_signals[arch.modules[symbol_interpolate].in0[0]]
                            mux_idx_in0 = mux_idx_in0 + 1
                            for mux_inputs in unroll(range(len(arch.modules[symbol_interpolate].in0))):
                                if in0_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in0))](mux_inputs):
                                    in0 = bit_signals[arch.modules[symbol_interpolate].in0[mux_inputs]]
                                
                        if inline(len(arch.modules[symbol_interpolate].in1) == 1):
                            in1 = bit_signals[arch.modules[symbol_interpolate].in1[0]]  
                        else:
                            in1_mux_select = inst.mux_in1[mux_idx_in1]
                            in1 = bit_signals[arch.modules[symbol_interpolate].in1[0]]
                            mux_idx_in1 = mux_idx_in1 + 1
                            for mux_inputs in unroll(range(len(arch.modules[symbol_interpolate].in1))):
                                if in1_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in1))](mux_inputs):
                                    in1 = bit_signals[arch.modules[symbol_interpolate].in1[mux_inputs]]

                        if inline(len(arch.modules[symbol_interpolate].in2) == 1):
                            in2 = bit_signals[arch.modules[symbol_interpolate].in2[0]]  
                        else:
                            in2_mux_select = inst.mux_in2[mux_idx_in2]
                            in2 = bit_signals[arch.modules[symbol_interpolate].in2[0]]
                            mux_idx_in2 = mux_idx_in2 + 1
                            for mux_inputs in unroll(range(len(arch.modules[symbol_interpolate].in2))):
                                if in2_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in2))](mux_inputs):
                                    in2 = bit_signals[arch.modules[symbol_interpolate].in2[mux_inputs]]

                        bit_signals[arch.modules[symbol_interpolate].id] = self.modules[symbol_interpolate](inst.lut[lut_idx], in0, in1, in2)
                        lut_idx = lut_idx + 1
                    else:

                        if inline(len(arch.modules[symbol_interpolate].in0) == 1):
                            in0 = signals[arch.modules[symbol_interpolate].in0[0]]  
                        else:
                            in0_mux_select = inst.mux_in0[mux_idx_in0]
                            in0 = signals[arch.modules[symbol_interpolate].in0[0]]
                            mux_idx_in0 = mux_idx_in0 + 1
                            for mux_inputs in unroll(range(len(arch.modules[symbol_interpolate].in0))):
                                if in0_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in0))](mux_inputs):
                                    in0 = signals[arch.modules[symbol_interpolate].in0[mux_inputs]]
                                
                        if inline(len(arch.modules[symbol_interpolate].in1) == 1):
                            in1 = signals[arch.modules[symbol_interpolate].in1[0]]  
                        else:
                            in1_mux_select = inst.mux_in1[mux_idx_in1]
                            in1 = signals[arch.modules[symbol_interpolate].in1[0]]
                            mux_idx_in1 = mux_idx_in1 + 1
                            for mux_inputs in unroll(range(len(arch.modules[symbol_interpolate].in1))):
                                if in1_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in1))](mux_inputs):
                                    in1 = signals[arch.modules[symbol_interpolate].in1[mux_inputs]]

                        if inline(arch.modules[symbol_interpolate].type_ == "mul"):
                            signals[arch.modules[symbol_interpolate].id] = self.modules[symbol_interpolate](inst.mul[mul_idx], inst.signed[signed_idx], in0, in1)
                            signed_idx = signed_idx + 1
                            mul_idx = mul_idx + 1
                            
                        elif inline(arch.modules[symbol_interpolate].type_ == "alu"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](inst.alu[alu_idx], inst.signed[signed_idx], in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = self.cond[cond_idx](inst.cond[cond_idx], alu_res_p, Z, N, C, V)
                            # res_p = bit_signals[arch.modules[symbol_interpolate].id]
                            cond_idx = cond_idx + 1
                            signed_idx = signed_idx + 1
                            alu_idx = alu_idx + 1
                        elif inline(arch.modules[symbol_interpolate].type_ == "bit_alu"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](inst.bit_alu[bit_alu_idx], in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = alu_res_p
                            bit_alu_idx = bit_alu_idx + 1

                        elif inline(arch.modules[symbol_interpolate].type_ == "fp_alu"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](inst.fp_alu[fp_alu_idx], inst.signed[signed_idx], in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = self.cond[cond_idx](inst.cond[cond_idx], alu_res_p, Z, N, C, V)
                            cond_idx = cond_idx + 1
                            signed_idx = signed_idx + 1
                            fp_alu_idx = fp_alu_idx + 1

                        elif inline(arch.modules[symbol_interpolate].type_ == "add"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = alu_res_p
                        elif inline(arch.modules[symbol_interpolate].type_ == "sub"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = self.cond[cond_idx](inst.cond[cond_idx], alu_res_p, Z, N, C, V)
                            cond_idx = cond_idx + 1
                        elif inline(arch.modules[symbol_interpolate].type_ == "abs"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](in0)
                            bit_signals[arch.modules[symbol_interpolate].id] = alu_res_p
                        elif inline(arch.modules[symbol_interpolate].type_ == "gte"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](inst.signed[signed_idx], in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = self.cond[cond_idx](inst.cond[cond_idx], alu_res_p, Z, N, C, V)
                            cond_idx = cond_idx + 1
                            signed_idx = signed_idx + 1
                        elif inline(arch.modules[symbol_interpolate].type_ == "lte"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](inst.signed[signed_idx], in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = self.cond[cond_idx](inst.cond[cond_idx], alu_res_p, Z, N, C, V)
                            cond_idx = cond_idx + 1
                            signed_idx = signed_idx + 1
                        elif inline(arch.modules[symbol_interpolate].type_ == "shr"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](inst.signed[signed_idx], in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = alu_res_p
                            signed_idx = signed_idx + 1
                        elif inline(arch.modules[symbol_interpolate].type_ == "shl"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = alu_res_p
                        elif inline(arch.modules[symbol_interpolate].type_ == "absd"):
                            signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules[symbol_interpolate](in0, in1)
                            bit_signals[arch.modules[symbol_interpolate].id] = alu_res_p

                        elif inline(arch.modules[symbol_interpolate].type_ == "mux"):

                            if inline(len(arch.modules[symbol_interpolate].in2) == 1):
                                in2 = bit_signals[arch.modules[symbol_interpolate].in2[0]]  
                            else:
                                sel_mux_select = inst.mux_in2[mux_idx_in2]
                                in2 = bit_signals[arch.modules[symbol_interpolate].in2[0]]
                                mux_idx_in2 = mux_idx_in2 + 1
                                for mux_inputs in unroll(range(len(arch.modules[symbol_interpolate].in2))):
                                    if sel_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in2))](mux_inputs):
                                        in2 = bit_signals[arch.modules[symbol_interpolate].in2[mux_inputs]]


                            signals[arch.modules[symbol_interpolate].id] = self.modules[symbol_interpolate](in0, in1, in2)
                                

                # Register assignment
                reg_mux_idx = 0
                for symbol_interpolate in unroll(range(arch.num_reg)):
                    if inline(len(arch.regs[symbol_interpolate].in_) == 1):
                        in_ = signals[arch.regs[symbol_interpolate].in_[0]]  
                    else:
                        in_mux_select = inst.mux_reg[reg_mux_idx]
                        in_ = signals[arch.regs[symbol_interpolate].in_[0]]
                        reg_mux_idx = reg_mux_idx + 1

                        for mux_inputs in unroll(range(len(arch.regs[symbol_interpolate].in_))):
                            if in_mux_select == family.BitVector[m.math.log2_ceil(len(arch.regs[symbol_interpolate].in_))](mux_inputs):
                                in_ = signals[arch.regs[symbol_interpolate].in_[mux_inputs]]
                            
                    signals[arch.regs[symbol_interpolate].id] = self.regs[symbol_interpolate](in_, clk_en)
                
                bit_reg_mux_idx = 0
                for symbol_interpolate in unroll(range(arch.num_bit_reg)):
                    if inline(len(arch.bit_regs[symbol_interpolate].in_) == 1):
                        in_ = bit_signals[arch.bit_regs[symbol_interpolate].in_[0]]  
                    else:
                        in_mux_select = inst.mux_bit_reg[bit_reg_mux_idx]
                        in_ = bit_signals[arch.bit_regs[symbol_interpolate].in_[0]]
                        bit_reg_mux_idx = bit_reg_mux_idx + 1

                        for mux_inputs in unroll(range(len(arch.bit_regs[symbol_interpolate].in_))):
                            if in_mux_select == family.BitVector[m.math.log2_ceil(len(arch.bit_regs[symbol_interpolate].in_))](mux_inputs):
                                in_ = bit_signals[arch.bit_regs[symbol_interpolate].in_[mux_inputs]]
                            
                    bit_signals[arch.bit_regs[symbol_interpolate].id] = self.bit_regs[symbol_interpolate](in_, clk_en)

                
                # Output assignment
                outputs = []
                bit_outputs = []
                mux_idx_out = 0
                mux_idx_bit_out = 0
                for out_index in unroll(range(arch.num_outputs)):
                    if inline(len(arch.outputs[out_index]) == 1):
                        outputs.append(signals[arch.outputs[out_index][0]])
                    elif inline(len(arch.outputs[out_index]) > 1):
                        output_temp = signals[arch.outputs[out_index][0]]
                        out_mux_select = inst.mux_out[mux_idx_out]
                        mux_idx_out = mux_idx_out + 1
                        for mux_inputs in unroll(range(len(arch.outputs[out_index]))):
                            if out_mux_select == family.BitVector[m.math.log2_ceil(len(arch.outputs[out_index]))](mux_inputs):
                                output_temp = signals[arch.outputs[out_index][mux_inputs]]
                        outputs.append(output_temp)


                for bit_out_index in unroll(range(arch.num_bit_outputs)):
                    if inline(len(arch.bit_outputs[bit_out_index]) == 1):
                        bit_outputs.append(bit_signals[arch.bit_outputs[bit_out_index][0]])
                    elif inline(len(arch.bit_outputs[bit_out_index]) > 1):
                        bit_output_temp = bit_signals[arch.bit_outputs[bit_out_index][0]]
                        out_mux_select = inst.mux_bit_out[mux_idx_bit_out]
                        mux_idx_bit_out = mux_idx_bit_out + 1
                        for mux_inputs in unroll(range(len(arch.bit_outputs[bit_out_index]))):
                            if out_mux_select == family.BitVector[m.math.log2_ceil(len(arch.bit_outputs[bit_out_index]))](mux_inputs):
                                bit_output_temp = bit_signals[arch.bit_outputs[bit_out_index][mux_inputs]]
                        bit_outputs.append(bit_output_temp)


                if inline(arch.enable_output_regs):
                    outputs_from_reg = []
                    for symbol_interpolate in unroll(range(arch.num_outputs)):
                        temp = self.output_regs[symbol_interpolate](outputs[symbol_interpolate], clk_en) 
                        outputs_from_reg.append(temp)
                    for symbol_interpolate in unroll(range(arch.num_bit_outputs)):
                        temp = self.bit_output_regs[symbol_interpolate](bit_outputs[symbol_interpolate], clk_en)
                        outputs_from_reg.append(temp)

                    # return 16-bit result, 1-bit result
                    return Output_Tc(*outputs_from_reg)
                    
                else:
                    outputs = outputs + bit_outputs
                    return Output_Tc(*outputs)

            fp_vals = Tuple[(fp_val for _ in range(arch.num_fp_alu))]

            # print(inspect.getsource(__init__)) 
            # print(inspect.getsource(__call__)) 
            @apply_passes([loop_unroll(), if_inline()])
            def _set_fp(self, fp_vals : fp_vals):
                i = 0
                for symbol_interpolate in unroll(range(len(arch.modules))):
                    if inline(arch.modules[symbol_interpolate].type_ == 'fp_alu'):
                        module = self.modules[symbol_interpolate]
                        module.fp_unit._set_fp(fp_vals[i].res, fp_vals[i].res_p, fp_vals[i].Z, fp_vals[i].N, fp_vals[i].C, fp_vals[i].V)
                        i += 1
                         

        return PE_gen
    return PE_fc


def fp_pe_arch_closure(arch):
    
    @family_closure
    def FP_PE_fc(family: AbstractFamily):
        BitVector = family.BitVector
        Data = family.BitVector[arch.input_width]
        Out_Data = family.BitVector[arch.output_width]
        Bit = family.Bit

        DataInputList = Tuple[(Data if i < arch.num_inputs else Bit for i in range(arch.num_inputs + arch.num_bit_inputs))]

        Output_T = Tuple[(Out_Data if i < arch.num_outputs else Bit for i in range(arch.num_outputs + arch.num_bit_outputs))]
        Output_Tc = family.get_constructor(Output_T)

        Inst_fc = inst_arch_closure(arch)
        Inst = Inst_fc(family)

        class fp_val(Product):
            res = Data
            res_p = Bit
            Z = Bit
            N = Bit
            C = Bit
            V = Bit        

        PE = pe_arch_closure(arch)(family)

        fp_vals_t = Tuple[(fp_val for _ in range(arch.num_fp_alu))]
        
        @family.assemble(locals(), globals())
        class FP_PE(Peak):
            def __init__(self):
                self.pe : PE = PE()

            @name_outputs(pe_outputs=Output_T)
            def __call__(self, fp_vals : fp_vals_t, inst : Const(Inst), inputs: DataInputList, \
                    # bit_inputs: BitInputList = BitInputListDefault, \
                    clk_en: Global(Bit) = Bit(1)) -> Output_T:


                self.pe._set_fp(fp_vals)
                return self.pe(inst, inputs, clk_en)

        return FP_PE
    return FP_PE_fc

    
