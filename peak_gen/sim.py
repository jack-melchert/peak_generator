from peak import Peak, family_closure, name_outputs, gen_register, Const
from hwtypes.adt import Tuple
from functools import lru_cache
import magma as m
import hwtypes
import ast_tools
from ast_tools.passes import begin_rewrite, end_rewrite, loop_unroll, if_inline
from ast_tools.macros import inline
import inspect
from .common import *
from .lut import LUT_fc
from .alu import ALU_fc
from .add import ADD_fc
from .cond import Cond_fc
from .isa import inst_arch_closure
from .arch import *
from .mul import MUL_fc
from .mux import MUX_fc
from peak.assembler import Assembler, AssembledADT
from peak.family import AbstractFamily
import peak 

def arch_closure(arch):
    @family_closure
    def PE_fc(family: AbstractFamily):

        BitVector = family.BitVector
        Data = family.BitVector[arch.input_width]
        Out_Data = family.BitVector[arch.output_width]
        UBit = family.Unsigned[1]
        Data8 = family.BitVector[8]
        Data32 = family.BitVector[32]
        UData32 = family.Unsigned[32]
        Bit = family.Bit
        Register = gen_register(Data, 0)(family)
        ALU_bw = ALU_fc(family)
        ADD_bw = ADD_fc(family)
        LUT = LUT_fc(family)
        MUL_bw = MUL_fc(family)
        MUX_bw = MUX_fc(family)
        Inst_fc = inst_arch_closure(arch)
        Inst = Inst_fc(family)
        Cond = Cond_fc(family)


        DataInputList = Tuple[(Data for _ in range(arch.num_inputs))]
        BitInputList = Tuple[(Bit for _ in range(arch.num_alu + 3))]

        BitInputListDefault = BitInputList(*[Bit(0) for _ in range(arch.num_alu + 3)])

        Output_T = Tuple[(Out_Data for _ in range(arch.num_outputs))]
        Output_Tc = family.get_constructor(Output_T)

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

                if inline(arch.enable_output_regs):
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_outputs)):
                        self.output_reg_symbol_interpolate: Register = Register()

                for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_reg)):
                    self.regs_symbol_interpolate: Register = Register()

                for symbol_interpolate in ast_tools.macros.unroll(range(len(arch.modules))):
                    if inline(arch.modules[symbol_interpolate].type_ == 'alu'):
                        self.modules_symbol_interpolate: type(ALU_bw(arch.input_width)) = ALU_bw(arch.modules[symbol_interpolate].in_width)()
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
            @name_outputs(PE_res=Output_T, res_p=Bit)
            def __call__(self, inst: Const(Inst), \
                inputs: DataInputList, \
                bit_inputs: BitInputList = BitInputListDefault, \
                clk_en: Global(Bit) = Bit(1)
            ) -> (Output_T, Bit):


                # calculate lut results
                lut_res = self.lut(inst.lut, bit_inputs[0], bit_inputs[1], bit_inputs[2])

                signals = {}
                bit_signals = {}

                #  Inputs with or without registers
                if inline(arch.enable_input_regs):
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_inputs)):
                        signals[arch.inputs[symbol_interpolate]] = self.input_reg_symbol_interpolate(inputs[symbol_interpolate], clk_en)
                        
                else:
                    for i in ast_tools.macros.unroll(range(arch.num_inputs)):
                        signals[arch.inputs[i]] = inputs[i]
                        
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
                        signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules_symbol_interpolate(inst.alu[alu_idx], inst.signed, in0, in1, bit_inputs[alu_idx + 3])
                        bit_signals[arch.modules[symbol_interpolate].id] = self.cond_symbol_interpolate(inst.cond[cond_idx], alu_res_p, lut_res, Z, N, C, V)
                        res_p = bit_signals[arch.modules[symbol_interpolate].id]
                        cond_idx = cond_idx + 1
                        alu_idx = alu_idx + 1

                    elif inline(arch.modules[symbol_interpolate].type_ == "add"):
                        signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules_symbol_interpolate(in0, in1)
                        bit_signals[arch.modules[symbol_interpolate].id] = self.cond_symbol_interpolate(inst.cond[cond_idx], alu_res_p, lut_res, Z, N, C, V)
                        res_p = bit_signals[arch.modules[symbol_interpolate].id]
                        cond_idx = cond_idx + 1

                    elif inline(arch.modules[symbol_interpolate].type_ == "mux"):
                        signals[arch.modules[symbol_interpolate].id] = self.modules_symbol_interpolate(in0, in1, bit_signals[arch.modules[symbol_interpolate].in2])
                            

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



                if inline(arch.enable_output_regs):
                    outputs_from_reg = []
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_outputs)):
                        temp = self.output_reg_symbol_interpolate(outputs[symbol_interpolate], clk_en)
                        outputs_from_reg.append(temp)

                    # return 16-bit result, 1-bit result
                    return Output_Tc(*outputs_from_reg), res_p
                    
                else:
                    return Output_Tc(*outputs), res_p

            # print(inspect.getsource(__init__)) 
            # print(inspect.getsource(__call__)) 
        return PE
    return PE_fc
