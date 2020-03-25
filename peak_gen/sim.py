from peak import Peak, family_closure, name_outputs, assemble, gen_register
from hwtypes import Tuple
from functools import lru_cache
import magma as m
import ast_tools
from ast_tools.passes import begin_rewrite, end_rewrite, loop_unroll, if_inline
from ast_tools.macros import inline
import inspect
from .common import *
from .mode import gen_register_mode
from .lut import LUT_fc
from .alu import ALU_fc
from .add import ADD_fc
from .cond import Cond_fc
from .isa import inst_arch_closure
from .arch import *
from .mul import MUL_fc
from .config import config_arch_closure
from .enables import enables_arch_closure

def arch_closure(arch):
    @family_closure
    def PE_fc(family):
        BitVector = family.BitVector

        #Hack
        def BV1(bit):
            return bit.ite(family.BitVector[1](1), family.BitVector[1](0))
        Data = family.BitVector[arch.input_width]
        Out_Data = family.BitVector[arch.output_width]
        UBit = family.Unsigned[1]
        Data8 = family.BitVector[8]
        Data32 = family.BitVector[32]
        UData32 = family.Unsigned[32]
        Bit = family.Bit
        ConstRegister = gen_register_mode(Data, 0)(family)
        Register = gen_register(Data, 0)(family)
        BitReg = gen_register_mode(Bit, 0)(family)
        ALU_bw = ALU_fc(family)
        ADD_bw = ADD_fc(family)
        LUT = LUT_fc(family)
        MUL_bw = MUL_fc(family)
        Inst_fc = inst_arch_closure(arch)
        Inst = Inst_fc(family)
        Config_fc = config_arch_closure(arch)
        Config = Config_fc(family)
        Enables_fc = enables_arch_closure(arch)
        Enables = Enables_fc(family)
        Cond = Cond_fc(family)


        DataInputList = Tuple[(Data for _ in range(arch.num_inputs))]
        DataOutputList = Tuple[(Out_Data for _ in range(arch.num_outputs))]
        ConfigDataList = Tuple[(Data for _ in range(arch.num_const_reg))]
        RegEnList = Tuple[(Bit for _ in range(arch.num_reg))]

        if arch.num_reg > 0:
            RegEnListDefault_temp = [Bit(1) for _ in range(arch.num_reg)]
            RegEnListDefault = Enables(Bit(1), RegEnList(*RegEnListDefault_temp))
        else:
            RegEnListDefault = Enables(Bit(1))


        Config_default_list = [Data(0) for _ in range(arch.num_const_reg)]
        if (arch.num_const_reg > 0):
            Config_default = Config(family.BitVector[3](0), ConfigDataList(*Config_default_list))
        else:
            Config_default = Config(family.BitVector[3](0))

        @assemble(family, locals(), globals())
        class PE(Peak):
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

                for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_const_reg)):
                    self.const_reg_symbol_interpolate: ConstRegister = ConstRegister()

                for symbol_interpolate in ast_tools.macros.unroll(range(len(arch.modules))):
                    if inline(arch.modules[symbol_interpolate].type_ == 'alu'):
                        self.modules_symbol_interpolate: type(ALU_bw(arch.input_width)) = ALU_bw(arch.modules[symbol_interpolate].in_width)()
                    if inline(arch.modules[symbol_interpolate].type_ == 'mul'):
                        self.modules_symbol_interpolate: type(MUL_bw(arch.modules[symbol_interpolate].in_width, arch.modules[symbol_interpolate].out_width)) = MUL_bw(arch.modules[symbol_interpolate].in_width, arch.modules[symbol_interpolate].out_width)()
                    if inline(arch.modules[symbol_interpolate].type_ == 'add'):
                        self.modules_symbol_interpolate: type(ALU_bw(arch.input_width)) = ADD_bw(arch.input_width)()
                # Bit Registers
                self.regd: BitReg = BitReg()
                self.rege: BitReg = BitReg()
                self.regf: BitReg = BitReg()

                #Condition code
                self.cond: Cond = Cond()

                #Lut
                self.lut: LUT = LUT()

            @end_rewrite()
            @if_inline()
            @loop_unroll()
            @loop_unroll()
            @begin_rewrite()
            @name_outputs(PE_res=Out_Data, res_p=UBit, read_config_data=UData32)
            def __call__(self, inst: Inst, \
                inputs : DataInputList, \
                enables : Enables = RegEnListDefault, \
                config_addr : Data8 = Data8(0), \
                config_data : Config = Config_default, \
                config_en : Bit = Bit(0) \
            ) -> (Out_Data, Bit, Data32):
                # Simulate one clock cycle


                bit012_addr = (config_addr[:3] == BitVector[3](BIT012_ADDR))

                # input registers
                reg_we = []

                for i in ast_tools.macros.unroll(range(arch.num_const_reg)):
                    reg_we.append((config_addr == BitVector[8](i)) & config_en)

                #rd
                rd_we = (bit012_addr & config_en)
                rd_config_wdata = config_data.config_data_bits[0]

                #re
                re_we = rd_we
                re_config_wdata = config_data.config_data_bits[1]

                #rf
                rf_we = rd_we
                rf_config_wdata = config_data.config_data_bits[2]

                signals = {}

                if inline(arch.enable_input_regs):
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_inputs)):
                        signals[arch.inputs[symbol_interpolate]] = self.input_reg_symbol_interpolate(inputs[symbol_interpolate], enables.clk_en)
                        
                else:
                    for i in ast_tools.macros.unroll(range(arch.num_inputs)):
                        signals[arch.inputs[i]] = inputs[i]
                        

                rd, rd_rdata = self.regd(rd_config_wdata, rd_we, enables.clk_en)
                re, re_rdata = self.rege(re_config_wdata, re_we, enables.clk_en)
                rf, rf_rdata = self.regf(rf_config_wdata, rf_we, enables.clk_en)


                for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_const_reg)):
                    signals[arch.const_regs[symbol_interpolate].id], _ = self.const_reg_symbol_interpolate(config_data.config_data[symbol_interpolate], reg_we[symbol_interpolate], enables.clk_en)

                #Calculate read_config_data
                read_config_data = BV1(rd_rdata).concat(BV1(re_rdata)).concat(BV1(rf_rdata)).concat(BitVector[32-3](0))


                for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_reg)):
                    signals[arch.regs[symbol_interpolate].id] = self.regs_symbol_interpolate(Data(0), 0)

   
                mux_idx_in0 = 0
                mux_idx_in1 = 0
                mul_idx = 0
                alu_idx = 0

                for symbol_interpolate in ast_tools.macros.unroll(range(len(arch.modules))):

                    if inline(len(arch.modules[symbol_interpolate].in0) == 1):
                        in0 = signals[arch.modules[symbol_interpolate].in0[0]]  
                    else:
                        in0_mux_select = inst.mux_in0[mux_idx_in0]
                        mux_idx_in0 = mux_idx_in0 + 1
                        for mux_inputs in ast_tools.macros.unroll(range(len(arch.modules[symbol_interpolate].in0))):
                            if in0_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in0))](mux_inputs):
                                in0 = signals[arch.modules[symbol_interpolate].in0[mux_inputs]]
                            
                    if inline(len(arch.modules[symbol_interpolate].in1) == 1):
                        in1 = signals[arch.modules[symbol_interpolate].in1[0]]  
                    else:
                        in1_mux_select = inst.mux_in1[mux_idx_in1]
                        mux_idx_in1 = mux_idx_in1 + 1
                        for mux_inputs in ast_tools.macros.unroll(range(len(arch.modules[symbol_interpolate].in1))):
                            if in1_mux_select == family.BitVector[m.math.log2_ceil(len(arch.modules[symbol_interpolate].in1))](mux_inputs):
                                in1 = signals[arch.modules[symbol_interpolate].in1[mux_inputs]]

                    if inline(arch.modules[symbol_interpolate].type_ == "mul"):
                        signals[arch.modules[symbol_interpolate].id] = self.modules_symbol_interpolate(inst.mul[mul_idx], inst.signed, in0, in1)
                        mul_idx = mul_idx + 1
                        
                    elif inline(arch.modules[symbol_interpolate].type_ == "alu"):
                        signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules_symbol_interpolate(inst.alu[alu_idx], inst.signed, in0, in1, rd)
                        alu_idx = alu_idx + 1

                    elif inline(arch.modules[symbol_interpolate].type_ == "add"):
                        signals[arch.modules[symbol_interpolate].id], alu_res_p, Z, N, C, V = self.modules_symbol_interpolate(in0, in1)
                            

                reg_mux_idx = 0

                for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_reg)):
                    if inline(len(arch.regs[symbol_interpolate].in_) == 1):
                        in_ = signals[arch.regs[symbol_interpolate].in_[0]]  
                    else:
                        in_mux_select = inst.mux_reg[reg_mux_idx]
                        reg_mux_idx = reg_mux_idx + 1

                        for mux_inputs in ast_tools.macros.unroll(range(len(arch.regs[symbol_interpolate].in_))):
                            if in_mux_select == family.BitVector[m.math.log2_ceil(len(arch.regs[symbol_interpolate].in_))](mux_inputs):
                                in_ = signals[arch.regs[symbol_interpolate].in_[mux_inputs]]
                            
                    signals[arch.regs[symbol_interpolate].id] = self.regs_symbol_interpolate(in_, enables.clk_en.ite(enables.reg_enables[symbol_interpolate], Bit(0)))

                # calculate lut results
                lut_res = self.lut(inst.lut, rd, re, rf)

                # calculate 1-bit result
                # alu_res_p = Bit(0) 
                # Z = Bit(0) 
                # N = Bit(0) 
                # C = Bit(0) 
                # V = Bit(0) 
                res_p = self.cond(inst.cond, alu_res_p, lut_res, Z, N, C, V)
                # res_p = Bit(0)
                
                outputs = []
                mux_idx_out = 0
                for out_index in ast_tools.macros.unroll(range(arch.num_outputs)):
                    if inline(len(arch.outputs[out_index]) == 1):
                        output_temp = signals[arch.outputs[out_index][0]]
                        outputs.append(output_temp)
                    else:
                        # output_temp = signals[arch.outputs[out_index][0]]
                        out_mux_select = inst.mux_out[mux_idx_out]
                        mux_idx_out = mux_idx_out + 1
                        for mux_inputs in ast_tools.macros.unroll(range(len(arch.outputs[out_index]))):
                            if out_mux_select == family.BitVector[m.math.log2_ceil(len(arch.outputs[out_index]))](mux_inputs):
                                output_temp = signals[arch.outputs[out_index][mux_inputs]]
                        outputs.append(output_temp)



                if inline(arch.enable_output_regs):
                    outputs_from_reg = []
                    for symbol_interpolate in ast_tools.macros.unroll(range(arch.num_outputs)):
                        temp = self.output_reg_symbol_interpolate(outputs[symbol_interpolate], enables.clk_en)
                        outputs_from_reg.append(temp)

                    # return 16-bit result, 1-bit result
                    # return DataOutputList(*outputs_from_reg), res_p, read_config_data
                else:
                    return outputs[0], res_p, read_config_data
                    # return DataOutputList(*outputs), res_p, read_config_data

            # print(inspect.getsource(__init__)) 
            print(inspect.getsource(__call__)) 
        return PE
    return PE_fc
