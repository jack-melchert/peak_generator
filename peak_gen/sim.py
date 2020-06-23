from peak import Peak, family_closure, name_outputs, gen_register, Const
from hwtypes.adt import Tuple, Product
from functools import lru_cache
import magma as m
import hwtypes
import ast_tools
from ast_tools.passes import begin_rewrite, end_rewrite, loop_unroll, if_inline
from ast_tools.macros import inline
import inspect
from .common import *
from .lut import LUT_fc
from .alu import ALU_fc, fp_unit_fc
from .alu_no_fp import ALU_no_fp_fc
from .add import ADD_fc
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
        fp_unit_bw = fp_unit_fc(family)
        ALU_no_fp_bw = ALU_no_fp_fc(family)
        ADD_bw = ADD_fc(family)
        LUT = LUT_fc(family)
        MUL_bw = MUL_fc(family)
        MUX_bw = MUX_fc(family)
        Inst_fc = inst_arch_closure(arch)
        Inst = Inst_fc(family)
        Cond = Cond_fc(family)

        DataInputList = Tuple[(Data for _ in range(arch.num_inputs))]
        BitInputList = Tuple[(Bit for _ in range(arch.num_bit_inputs + 3))]

        BitInputListDefault = BitInputList(*[Bit(0) for _ in range(arch.num_bit_inputs + 3)])

        Output_T = Tuple[(Out_Data if i < arch.num_outputs else Bit for i in range(arch.num_outputs + arch.num_bit_outputs))]
        Output_Tc = family.get_constructor(Output_T)

        class fp_val(Product):
            res = Data
            res_p = Bit
            Z = Bit
            N = Bit
            C = Bit
            V = Bit  

        # Bit_Output_T = Tuple[(Bit for _ in range(arch.num_bit_outputs))]
        # Bit_Output_Tc = family.get_constructor(Bit_Output_T)

        @family.assemble(locals(), globals())
        class PE(Peak, typecheck=True):
            @end_rewrite()
            @if_inline()
            @loop_unroll()
            @begin_rewrite()
            def __init__(self):

                # Data registers
                if inline(arch.enable_input_regs):
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_inputs)):
                        self.input_reg_symbol_interpolate: Register = Register()
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_bit_inputs)):
                        self.bit_input_reg_symbol_interpolate: Bit_Register = Bit_Register()

                if inline(arch.enable_output_regs):
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_outputs)):
                        self.output_reg_symbol_interpolate: Register = Register()
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_bit_outputs)):
                        self.bit_output_reg_symbol_interpolate: Bit_Register = Bit_Register()

                for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_reg)):
                    self.regs_symbol_interpolate: Register = Register()

                for symbol_interpolate in ast_tools.macros.unroll(range(len(arch.modules))):
                    if inline(arch.modules[symbol_interpolate].type_ == 'alu'):
                        if inline(arch.modules[symbol_interpolate].in_width == 16):
                            self.modules_symbol_interpolate: type(ALU_bw(arch.modules[symbol_interpolate].in_width)) = ALU_bw(arch.modules[symbol_interpolate].in_width)()
                        else:
                            self.modules_symbol_interpolate: type(ALU_no_fp_bw(arch.modules[symbol_interpolate].in_width)) = ALU_no_fp_bw(arch.modules[symbol_interpolate].in_width)()
                        self.cond_symbol_interpolate: Cond = Cond()
                    if inline(arch.modules[symbol_interpolate].type_ == 'mul'):
                        self.modules_symbol_interpolate: type(MUL_bw(arch.modules[symbol_interpolate].in_width, arch.modules[symbol_interpolate].out_width)) = MUL_bw(arch.modules[symbol_interpolate].in_width, arch.modules[symbol_interpolate].out_width)()
                    if inline(arch.modules[symbol_interpolate].type_ == 'add'):
                        self.modules_symbol_interpolate: type(ALU_bw(arch.input_width)) = ADD_bw(arch.input_width)()
                        self.cond_symbol_interpolate: Cond = Cond()
                    if inline(arch.modules[symbol_interpolate].type_ == 'mux'):
                        self.modules_symbol_interpolate: type(MUX_bw(arch.input_width)) = MUX_bw(arch.input_width)()

                #Lut
                self.lut: LUT = LUT()

            @end_rewrite()
            @if_inline()
            @loop_unroll()
            @loop_unroll()
            @begin_rewrite()
            @name_outputs(pe_outputs=Output_T)
            def __call__(self, inst: Const(Inst), \
                inputs: DataInputList, \
                bit_inputs: BitInputList = BitInputListDefault, \
                clk_en: Global(Bit) = Bit(1)
            ) -> (Output_T):


                # calculate lut results
                lut_res = self.lut(inst.lut, bit_inputs[0], bit_inputs[1], bit_inputs[2])

                signals = {}
                bit_signals = {}

                #  Inputs with or without registers
                if inline(arch.enable_input_regs):
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_inputs)):
                        signals[arch.inputs[symbol_interpolate]] = self.input_reg_symbol_interpolate(inputs[symbol_interpolate], clk_en)
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_bit_inputs)):
                        signals[arch.bit_inputs[symbol_interpolate]] = self.bit_input_reg_symbol_interpolate(bit_inputs[symbol_interpolate + 3], clk_en)
                        
                else:
                    for i in ast_tools.macros.unroll(range(arch.num_inputs)):
                        signals[arch.inputs[i]] = inputs[i]
                    for i in ast_tools.macros.unroll(range(arch.num_bit_inputs)):
                        signals[arch.bit_inputs[i]] = bit_inputs[i + 3]
                        
                # Constant inputs
                for i in ast_tools.macros.unroll(range(arch.num_const_inputs)):
                    signals[arch.const_inputs[i].id] = inst.const_data[i]

                # Pipelining registers
                for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_reg)):
                    signals[arch.regs[symbol_interpolate].id] = self.regs_symbol_interpolate(Data(0), Bit(0))

   
                mux_idx_in0 = 0
                mux_idx_in1 = 0
                mul_idx = 0
                alu_idx = 0
                cond_idx = 0
                res_p = Bit(0)
                Z = Bit(0)
                N = Bit(0)
                C = Bit(0)
                V = Bit(0)

                # Loop over modules (ALU, MUL, Adders, etc.)
                for symbol_interpolate in ast_tools.macros.unroll(range(len(arch.modules))):

                    if inline(len(arch.modules[symbol_interpolate].in0) == 1):
                        in0 = signals[arch.modules[symbol_interpolate].in0[0]]  
                    else:
                        in0_mux_select = inst.mux_in0[mux_idx_in0]
                        in0 = signals[arch.modules[symbol_interpolate].in0[0]]
                        mux_idx_in0 = mux_idx_in0 + 1
                        for mux_inputs in ast_tools.macros.unroll(range(len(arch.modules[symbol_interpolate].in0))):
                            if in0_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in0))](mux_inputs):
                                in0 = signals[arch.modules[symbol_interpolate].in0[mux_inputs]]
                            
                    if inline(len(arch.modules[symbol_interpolate].in1) == 1):
                        in1 = signals[arch.modules[symbol_interpolate].in1[0]]  
                    else:
                        in1_mux_select = inst.mux_in1[mux_idx_in1]
                        in1 = signals[arch.modules[symbol_interpolate].in1[0]]
                        mux_idx_in1 = mux_idx_in1 + 1
                        for mux_inputs in ast_tools.macros.unroll(range(len(arch.modules[symbol_interpolate].in1))):
                            if in1_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in1))](mux_inputs):
                                in1 = signals[arch.modules[symbol_interpolate].in1[mux_inputs]]

                    if inline(arch.modules[symbol_interpolate].type_ == "mul"):
                        signals[arch.modules[symbol_interpolate].id] = self.modules_symbol_interpolate(inst.mul[mul_idx], inst.signed, in0, in1)
                        mul_idx = mul_idx + 1
                        
                    elif inline(arch.modules[symbol_interpolate].type_ == "alu"):
                        signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules_symbol_interpolate(inst.alu[alu_idx], inst.signed, in0, in1)
                        bit_signals[arch.modules[symbol_interpolate].id] = self.cond_symbol_interpolate(inst.cond[cond_idx], alu_res_p, lut_res, Z, N, C, V)
                        # res_p = bit_signals[arch.modules[symbol_interpolate].id]
                        cond_idx = cond_idx + 1
                        alu_idx = alu_idx + 1

                    elif inline(arch.modules[symbol_interpolate].type_ == "add"):
                        signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules_symbol_interpolate(in0, in1)
                        bit_signals[arch.modules[symbol_interpolate].id] = self.cond_symbol_interpolate(inst.cond[cond_idx], alu_res_p, lut_res, Z, N, C, V)
                        # res_p = bit_signals[arch.modules[symbol_interpolate].id]
                        cond_idx = cond_idx + 1

                    elif inline(arch.modules[symbol_interpolate].type_ == "mux"):
                        signals[arch.modules[symbol_interpolate].id] = self.modules_symbol_interpolate(in0, in1, bit_signals[arch.modules[symbol_interpolate].sel])
                            

                # Register assignment
                reg_mux_idx = 0
                for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_reg)):
                    if inline(len(arch.regs[symbol_interpolate].in_) == 1):
                        in_ = signals[arch.regs[symbol_interpolate].in_[0]]  
                    else:
                        in_mux_select = inst.mux_reg[reg_mux_idx]
                        in_ = signals[arch.regs[symbol_interpolate].in_[0]]
                        reg_mux_idx = reg_mux_idx + 1

                        for mux_inputs in ast_tools.macros.unroll(range(len(arch.regs[symbol_interpolate].in_))):
                            if in_mux_select == family.BitVector[m.math.log2_ceil(len(arch.regs[symbol_interpolate].in_))](mux_inputs):
                                in_ = signals[arch.regs[symbol_interpolate].in_[mux_inputs]]
                            
                    signals[arch.regs[symbol_interpolate].id] = self.regs_symbol_interpolate(in_, clk_en)

                
                # Output assignment
                outputs = []
                bit_outputs = []
                mux_idx_out = 0
                for out_index in ast_tools.macros.unroll(range(arch.num_outputs)):
                    if inline(len(arch.outputs[out_index]) == 1):
                        outputs.append(signals[arch.outputs[out_index][0]])
                    else:
                        output_temp = signals[arch.outputs[out_index][0]]
                        out_mux_select = inst.mux_out[mux_idx_out]
                        mux_idx_out = mux_idx_out + 1
                        for mux_inputs in ast_tools.macros.unroll(range(len(arch.outputs[out_index]))):
                            if out_mux_select == family.BitVector[m.math.log2_ceil(len(arch.outputs[out_index]))](mux_inputs):
                                output_temp = signals[arch.outputs[out_index][mux_inputs]]
                        outputs.append(output_temp)

                for out_index in ast_tools.macros.unroll(range(arch.num_bit_outputs)):
                    bit_outputs.append(bit_signals[arch.bit_outputs[out_index]])


                if inline(arch.enable_output_regs):
                    outputs_from_reg = []
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_outputs)):
                        temp = self.output_reg_symbol_interpolate(outputs[symbol_interpolate], clk_en) 
                        outputs_from_reg.append(temp)
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_bit_outputs)):
                        temp = self.bit_output_reg_symbol_interpolate(bit_outputs[symbol_interpolate], clk_en)
                        outputs_from_reg.append(temp)

                    # return 16-bit result, 1-bit result
                    return Output_Tc(*outputs_from_reg)
                    
                else:
                    outputs = outputs + bit_outputs
                    return Output_Tc(*outputs)


      
                
            num_fp = 0
            for m in ast_tools.macros.unroll(range(len(arch.modules))):
                if arch.modules[m].type_ == 'alu':
                    if arch.modules[m].in_width == 16:
                        num_fp += 1

            fp_vals = Tuple[(fp_val for _ in range(num_fp))]

            # print(inspect.getsource(__init__)) 
            # print(inspect.getsource(__call__)) 
            @end_rewrite()
            @if_inline()
            @loop_unroll()
            @begin_rewrite()
            def _set_fp(self, fp_vals : fp_vals):
                i = 0
                for symbol_interpolate in ast_tools.macros.unroll(range(len(arch.modules))):
                    if inline(arch.modules[symbol_interpolate].type_ == 'alu'):
                        if inline(arch.modules[symbol_interpolate].in_width == 16):
                            module = self.modules_symbol_interpolate
                            module.fp_unit._set_fp(fp_vals[i].res, fp_vals[i].res_p, fp_vals[i].Z, fp_vals[i].N, fp_vals[i].C, fp_vals[i].V)
                            i += 1
                         

        return PE
    return PE_fc


def wrapped_pe_arch_closure(arch):
    
    @family_closure
    def Wrapped_PE_fc(family: AbstractFamily):
        BitVector = family.BitVector
        Data = family.BitVector[arch.input_width]
        Out_Data = family.BitVector[arch.output_width]
        Bit = family.Bit

        DataInputList = Tuple[(Data for _ in range(arch.num_inputs))]
        BitInputList = Tuple[(Bit for _ in range(arch.num_bit_inputs + 3))]

        BitInputListDefault = BitInputList(*[Bit(0) for _ in range(arch.num_bit_inputs + 3)])

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

        num_fp = 0
        for m in ast_tools.macros.unroll(range(len(arch.modules))):
            if arch.modules[m].type_ == 'alu':
                if arch.modules[m].in_width == 16:
                    num_fp += 1

        fp_vals = Tuple[(fp_val for _ in range(num_fp))]
        
        @family.assemble(locals(), globals())
        class Wrapped_PE(Peak):
            def __init__(self):
                self.pe : PE = PE()

            def __call__(self, fp_vals : fp_vals, inst : Const(Inst), inputs: DataInputList, \
                    bit_inputs: BitInputList = BitInputListDefault, \
                    clk_en: Global(Bit) = Bit(1)) -> Output_T:


                self.pe._set_fp(fp_vals)
                return self.pe(inst, inputs, bit_inputs, clk_en)

        return Wrapped_PE
    return Wrapped_PE_fc