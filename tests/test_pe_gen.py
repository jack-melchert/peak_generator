# import fault
# import magma
# import shutil
# from peak.assembler import Assembler, MagmaADT
# from peak import wrap_with_disassembler
# from peak_gen import pe_arch_closure, inst_arch_closure
# from peak_gen.arch import read_arch
# from peak_gen.asm import asm_arch_closure
# from peak_gen.alu import ALU_t, Signed_t
# from peak_gen.mul import MUL_t
# from peak_gen.cond import Cond_t
# from hwtypes import Bit, BitVector
# from hwtypes.adt import Tuple
# from peak import family
# import os
# import sys
# import random
# import pytest
# import glob

# class HashableDict(dict):
#     def __hash__(self):
#         return hash(tuple(sorted(self.keys())))

# @pytest.mark.parametrize("arch_file", glob.glob('examples/**/*.json', recursive=True))
# def test_pe_gen(arch_file):
#     arch = read_arch(arch_file)
#     width = arch.input_width
#     num_inputs = arch.num_inputs


#     num_outputs = arch.num_outputs

#     num_alu = arch.num_alu
#     Inst_fc = inst_arch_closure(arch)
#     Inst = Inst_fc(family.PyFamily())
#     asm_fc = asm_arch_closure(arch)
#     gen_inst = asm_fc(family.PyFamily())


#     PE_fc = pe_arch_closure(arch)
#     PE_bv = PE_fc(family.PyFamily())


#     Data = magma.BitVector[width]

#     # create these variables in global space so that we can reuse them easily
#     inst_name = 'inst'
#     inst_type = PE_bv.input_t.field_dict[inst_name]

#     _assembler = Assembler(inst_type)
#     assembler = _assembler.assemble
#     disassembler = _assembler.disassemble
#     # width = _assembler.width
#     layout = _assembler.layout


#     magma.backend.coreir_.CoreIRContextSingleton().reset_instance()
#     cw_dir = "/cad/synopsys/dc_shell/J-2014.09-SP3/dw/sim_ver/"   # noqa
#     CAD_ENV = shutil.which("ncsim") and os.path.isdir(cw_dir)


#     def copy_file(src_filename, dst_filename, override=False):
#         if not override and os.path.isfile(dst_filename):
#             return
#         shutil.copy(src_filename, dst_filename)


#     # Define instruction here
#     num_sim_cycles = 1
#     alu_list = [ALU_t.Add for _ in range(arch.num_alu)]
#     cond_list = [Cond_t.Z for _ in range(arch.num_alu + arch.num_add)]
#     mul_list = [MUL_t.Mult0 for _ in range(arch.num_mul)]
#     const_list = [Data(0) for _ in range(arch.num_const_inputs)]
#     mux_list_in0 = [0 for _ in range(arch.num_mux_in0)]
#     mux_list_in1 = [0 for _ in range(arch.num_mux_in1)]
#     mux_list_reg = [0 for _ in range(arch.num_reg_mux)]
#     mux_list_out = [0 for _ in range(arch.num_output_mux)]

#     # Enables_fc = enables_arch_closure(arch)
#     # Enables = Enables_fc(family.MagmaFamily())
#     # RegEnList = Tuple[(magma.Bit for _ in range(arch.num_reg))]

#     # if arch.num_reg > 0:
#     #     RegEnListDefault_temp = [magma.Bit(1) for _ in range(arch.num_reg)]
#     #     RegEnListDefault = Enables(magma.Bit(1), RegEnList(*RegEnListDefault_temp))
#     # else:
#     #     RegEnListDefault = Enables(magma.Bit(1))

#     mux_list_inst_in0 = []
#     mux_list_inst_in1 = []
#     mux_list_inst_reg = []
#     mux_list_inst_out = []

#     mux_0_idx = 0
#     mux_1_idx = 0
#     for i in range(len(arch.modules)):
#         if len(arch.modules[i].in0) > 1:
#             mux_list_inst_in0.append(BitVector[magma.math.log2_ceil(len(arch.modules[i].in0))](mux_list_in0[mux_0_idx]))
#             mux_0_idx += 1
#         if len(arch.modules[i].in1) > 1:   
#             mux_list_inst_in1.append(BitVector[magma.math.log2_ceil(len(arch.modules[i].in1))](mux_list_in1[mux_1_idx]))
#             mux_1_idx += 1

#     mux_reg_idx = 0
#     for i in range(len(arch.regs)):
#         if len(arch.regs[i].in_) > 1:
#             mux_list_inst_reg.append(BitVector[magma.math.log2_ceil(len(arch.regs[i].in_))](mux_list_reg[mux_reg_idx]))
#             mux_reg_idx += 1


#     mux_out_idx = 0
#     for i in range(num_outputs):
#         if len(arch.outputs[i]) > 1:
#             mux_list_inst_out.append(BitVector[magma.math.log2_ceil(len(arch.outputs[i]))](mux_list_out[mux_out_idx]))
#             mux_out_idx += 1


#     inst_gen = gen_inst(alu = alu_list, cond = cond_list, mul = mul_list, const = const_list, mux_in0 = mux_list_inst_in0, mux_in1 = mux_list_inst_in1, mux_reg = mux_list_inst_reg, mux_out = mux_list_inst_out, signed = Signed_t.unsigned, lut = 0)

#     inputs = [random.randint(0, 2**(width-2)) for _ in range(num_inputs)]

#     inputs_to_PE = [Data(inputs[i]) for i in range(num_inputs)]
#     print(inputs)

#     signals = {}
#     signals_new = {}

#     for i in arch.regs:
#         signals_new[i.id] = 0

#     for const_reg in arch.const_inputs:
#         signals_new[const_reg.id] = 0

#     for cyc in range(num_sim_cycles):

#         signals = signals_new.copy()

#         for i in range(num_inputs):
#             signals[arch.inputs[i]] = inputs[i]
    
#         mux_idx_in0 = 0
#         mux_idx_in1 = 0
#         for mod in range(len(arch.modules)):

#             if len(arch.modules[mod].in0) == 1:
#                 in0 = signals[arch.modules[mod].in0[0]]  
#             else:
#                 in0_mux_select = mux_list_in0[mux_idx_in0]
#                 mux_idx_in0 = mux_idx_in0 + 1
#                 for mux_inputs in range(len(arch.modules[mod].in0)):
#                     if in0_mux_select == mux_inputs:
#                         in0 = signals[arch.modules[mod].in0[mux_inputs]]

#             if len(arch.modules[mod].in1) == 1:
#                 in1 = signals[arch.modules[mod].in1[0]]  
#             else:
#                 in1_mux_select = mux_list_in1[mux_idx_in1]
#                 mux_idx_in1 = mux_idx_in1 + 1
#                 for mux_inputs in range(len(arch.modules[mod].in1)):
#                     if in1_mux_select == mux_inputs:
#                         in1 = signals[arch.modules[mod].in1[mux_inputs]]

#             if (arch.modules[mod].type_ == "mul"):
#                 signals[arch.modules[mod].id] = in0 * in1
#             elif (arch.modules[mod].type_ == "alu"):
#                 signals[arch.modules[mod].id] = in0 + in1
#             elif (arch.modules[mod].type_ == "add"):
#                 signals[arch.modules[mod].id] = in0 + in1
#             elif (arch.modules[mod].type_ == "mux"):
#                 signals[arch.modules[mod].id] = in1 if signals[arch.modules[mod].sel] == 0 else in0

#         signals_new = signals.copy()
#         mux_idx_reg = 0
#         for reg in arch.regs:
#             if len(reg.in_) == 1:
#                 in_ = signals[reg.in_[0]]  
#             else:
#                 in_mux_select = mux_list_reg[mux_idx_reg]
#                 mux_idx_reg = mux_idx_reg + 1
#                 for mux_inputs in range(len(reg.in_)):
#                     if in_mux_select == mux_inputs:
#                         in_ = signals[reg.in_[mux_inputs]]
#             signals_new[reg.id] = in_


#         res_comp = []

#         mux_idx_out = 0
#         for out in arch.outputs:
#             if len(out) == 1:
#                 res_comp.append(signals[out[0]])
#             else:
#                 out_mux_select = mux_list_out[mux_idx_out]
#                 mux_idx_out = mux_idx_out + 1
#                 for out_inputs in range(len(out)):
#                     if out_mux_select == out_inputs:
#                         res_comp.append(signals[out[out_inputs]])


#         res_comp = [Data(res) for res in res_comp]
#         print("Int test result: cycle", cyc, "=", res_comp)

#         pe = PE_bv()
#         for _ in range(num_sim_cycles):
#             res_pe = pe(inst_gen, inputs_to_PE)

#         # Need to advance clock cycles if regs are enabled
#         if (arch.enable_input_regs):
#             res_pe = pe(inst_gen, inputs_to_PE)
#         if (arch.enable_output_regs):
#             res_pe = pe(inst_gen, inputs_to_PE)

#         print("functional test result: ", [res_pe[i].value for i in range(num_outputs)])
#         assert res_comp  == [res_pe[i].value for i in range(num_outputs)] 


#         # PE_magma = PE_fc(family.MagmaFamily())
#         # instr_magma_type = type(PE_magma.interface.ports[inst_name])
#         # pe_circuit = wrap_with_disassembler(PE_magma, disassembler, width,
#         #                                         HashableDict(layout),
#         #                                         instr_magma_type)
#         # tester = fault.Tester(pe_circuit, clock=pe_circuit.CLK)
#         # test_dir = "tests/build"

#         # tester.clear()
#         # # Advance timestep past 0 for fp functional model (see rnd logic)
#         # tester.circuit.ASYNCRESET = 0
#         # tester.eval()
#         # tester.circuit.ASYNCRESET = 1
#         # tester.eval()
#         # tester.circuit.ASYNCRESET = 0
#         # tester.eval()


#         # DataInputList = Tuple[(Data for _ in range(arch.num_inputs))]
#         # asm_adt = Assembler(DataInputList)


#         # # tester.circuit.inputs = asm_adt.assemble(DataInputList(*inputs_to_PE))
#         # # tester.circuit.inst = assembler(inst_gen)
#         # tester.circuit.CLK = 0

#         # # import pdb; pdb.set_trace()
#         # tester.eval()

#         # if (arch.enable_input_regs):
#         #     tester.step(2)

#         # if (arch.enable_output_regs):
#         #     tester.step(2)

#         # for _ in range(num_sim_cycles - 1):
#         #     tester.step(2)
            
#         # tester.circuit.O0.expect(magma.BitVector[16](0))
        
            

#         # tester.compile_and_run("system-verilog", simulator="ncsim", directory=test_dir)



# test_pe_gen("examples/misc_tests/test_alu.json")