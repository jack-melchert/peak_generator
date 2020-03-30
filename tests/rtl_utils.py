import fault
import magma
import shutil
from peak.assembler import Assembler
from peak import wrap_with_disassembler
from peak_gen import arch_closure, inst_arch_closure
from peak_gen.arch import read_arch
from peak_gen.asm import asm_arch_closure
from peak_gen.alu import ALU_t_fc
from peak_gen.mul import MUL_t_fc
from peak_gen.enables import enables_arch_closure
from hwtypes import Bit, BitVector
import os

class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.keys())))


arch = read_arch(str(sys.argv[1]))
width = arch.input_width

Inst_fc = inst_arch_closure(arch)
Inst = Inst_fc(Bit.get_family())

PE_fc = arch_closure(arch)
PE_bv = PE_fc(Bit.get_family())

Data = BitVector[width]

# create these variables in global space so that we can reuse them easily
inst_name = 'inst'
inst_type = PE_bv.input_t.field_dict[inst_name]

_assembler = Assembler(inst_type)
assembler = _assembler.assemble
disassembler = _assembler.disassemble
width = _assembler.width
layout = _assembler.layout

PE_magma = PE_fc(magma.get_family())
instr_magma_type = type(PE_magma.interface.ports[inst_name])
pe_circuit = wrap_with_disassembler(PE_magma, disassembler, width,
                                         HashableDict(layout),
                                         instr_magma_type)
tester = fault.Tester(pe_circuit, clock=pe_circuit.CLK)
test_dir = "tests/build"

Mul_t = MUL_t_fc(Bit.get_family())
ALU_t, Signed_t = ALU_t_fc(Bit.get_family())


def copy_file(src_filename, dst_filename, override=False):
    if not override and os.path.isfile(dst_filename):
        return
    shutil.copy(src_filename, dst_filename)


def rtl_tester( alu_list = [ALU_t.Add for _ in range(arch.num_alu)], mul_list = [MUL_t.Mult0 for _ in range(arch.num_mul)], \
                input_data = [Data(0) for _ in range(arch.num_inputs)], config_data_bits = BitVector.random(0), \
                res_comp=None, res_p=None, clk_en=1, \
                mux_list_in0 = [0 for _ in range(arch.num_mux_in0)], mux_list_in1 = [0 for _ in range(arch.num_mux_in1)], \
                mux_list_reg = [0 for _ in range(arch.num_reg_mux)], mux_list_out = [0 for _ in range(arch.num_output_mux)], \
                enable_regs = 1, num_sim_cycles = 1):


    Enables_fc = enables_arch_closure(arch)
    Enables = Enables_fc(magma.get_family())
    RegEnList = Tuple[(magma.Bit for _ in range(arch.num_reg))]

    if arch.num_reg > 0:
        RegEnListDefault_temp = [magma.Bit(enable_regs) for _ in range(arch.num_reg)]
        RegEnListDefault = Enables(magma.Bit(clk_en), RegEnList(*RegEnListDefault_temp))
    else:
        RegEnListDefault = Enables(magma.Bit(clk_en))

    mux_list_inst_in0 = []
    mux_list_inst_in1 = []
    mux_list_inst_reg = []
    mux_list_inst_out = []

    mux_0_idx = 0
    mux_1_idx = 0
    for i in range(len(arch.modules)):
        if len(arch.modules[i].in0) > 1:
            mux_list_inst_in0.append(BitVector[magma.math.log2_ceil(len(arch.modules[i].in0))](mux_list_in0[mux_0_idx]))
            mux_0_idx += 1
        if len(arch.modules[i].in1) > 1:   
            mux_list_inst_in1.append(BitVector[magma.math.log2_ceil(len(arch.modules[i].in1))](mux_list_in1[mux_1_idx]))
            mux_1_idx += 1

    mux_reg_idx = 0
    for i in range(len(arch.regs)):
        if len(arch.regs[i].in_) > 1:
            mux_list_inst_reg.append(BitVector[magma.math.log2_ceil(len(arch.regs[i].in_))](mux_list_reg[mux_reg_idx]))
            mux_reg_idx += 1


    mux_out_idx = 0
    for i in range(num_outputs):
        if len(arch.outputs[i]) > 1:
            mux_list_inst_out.append(BitVector[magma.math.log2_ceil(len(arch.outputs[i]))](mux_list_out[mux_out_idx]))
            mux_out_idx += 1


    inst_gen = gen_inst(alu_list, mul_list, mux_list_inst_in0, mux_list_inst_in1, mux_list_inst_reg, mux_list_inst_out, Signed_t.unsigned, 0, Cond_t.Z)

    config_data_input = config(config_data_bits)


    tester.clear()
    # Advance timestep past 0 for fp functional model (see rnd logic)
    tester.circuit.ASYNCRESET = 0
    tester.eval()
    tester.circuit.ASYNCRESET = 1
    tester.eval()
    tester.circuit.ASYNCRESET = 0
    tester.eval()

    # import pdb; pdb.set_trace()
    tester.circuit.inst = assembler(inst_gen)
    tester.circuit.config_data = config_data_input
    tester.circuit.CLK = 0
    tester.circuit.enables = RegEnListDefault

    # import pdb; pdb.set_trace()
    tester.circuit.inputs = input_data
    tester.eval()

    if (arch.enable_input_regs):
        tester.step(2)

    if (arch.enable_output_regs):
        tester.step(2)

    for _ in range(num_sim_cycles - 1):
        tester.step(2)
        
    tester.circuit.O0.expect(res_comp)


    if False:
        # use ncsim
        libs = ["DW_fp_mult.v", "DW_fp_add.v", "DW_fp_addsub.v"]
        for filename in libs:
            copy_file(os.path.join(cw_dir, filename),
                      os.path.join(test_dir, filename))
        tester.compile_and_run(target="system-verilog", simulator="ncsim",
                               directory="tests/build/",
                               include_verilog_libraries=libs,
                               skip_compile=True)
    else:
        libs = ["DW_fp_mult.v", "DW_fp_add.v"]
        for filename in libs:
            copy_file(os.path.join("stubs", filename),
                      os.path.join(test_dir, filename))
        # # detect if the PE circuit has been built
        # skip_verilator = os.path.isfile(os.path.join(test_dir, "obj_dir",
        #                                              "VWrappedPE__ALL.a"))
        tester.compile_and_run(target="verilator",
                               directory=test_dir,
                               flags=['-Wno-UNUSED', '-Wno-PINNOCONNECT'],
                               skip_compile=False,
                               skip_verilator=False)