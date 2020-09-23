import fault
import magma
import shutil
from peak.assembler import Assembler
from peak import wrap_with_disassembler
from peak import family
from peak_gen import pe_arch_closure, inst_arch_closure
from peak_gen.arch import read_arch
from peak_gen.peak_wrapper import wrapped_peak_class
from hwtypes import Bit, BitVector, Tuple
import os

class HashableDict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.keys())))


def copy_file(src_filename, dst_filename, override=False):
    if not override and os.path.isfile(dst_filename):
        return
    shutil.copy(src_filename, dst_filename)


def rtl_tester(arch, inst, input_data, res_comp, num_sim_cycles = 1):

    shutil.rmtree("tests/build")

    PE_fc = wrapped_peak_class(arch)
    PE_bv = PE_fc.Py()

    inst_name = 'inst'
    inst_type = PE_bv.__call__._input_t.field_dict[inst_name]

    _assembler = Assembler(inst_type)
    assembler = _assembler.assemble
    disassembler = _assembler.disassemble
    width = _assembler.width
    layout = _assembler.layout

    PE_magma = PE_fc(family.MagmaFamily())
    instr_magma_type = type(PE_magma.interface.ports[inst_name])
    pe_circuit = wrap_with_disassembler(PE_magma, disassembler, width,
                                            HashableDict(layout),
                                            instr_magma_type)
    test_dir = "tests/build"
    magma.backend.coreir_.CoreIRContextSingleton().reset_instance()
    # magma.compile(f"{test_dir}/WrappedPE", pe_circuit, output="coreir-verilog")
    tester = fault.Tester(pe_circuit, clock=pe_circuit.CLK)

    Data = magma.BitVector[arch.input_width]
    DataInputList = Tuple[(Data for _ in range(arch.num_inputs))]
    asm_adt = Assembler(DataInputList)


    tester.clear()
    # Advance timestep past 0 for fp functional model (see rnd logic)
    tester.circuit.ASYNCRESET = 0
    tester.eval()
    tester.circuit.ASYNCRESET = 1
    tester.eval()
    tester.circuit.ASYNCRESET = 0
    tester.eval()
    tester.circuit.inst = assembler(inst)
    tester.circuit.CLK = 0
    tester.circuit.clk_en = 1

    tester.circuit.inputs0 = input_data[0]
    tester.circuit.inputs1 = input_data[1]
    tester.eval()

    if (arch.enable_input_regs):
        tester.step(2)

    if (arch.enable_output_regs):
        tester.step(2)

    for _ in range(num_sim_cycles - 1):
        tester.step(2)

    tester.circuit.O.expect(res_comp)


    tester.compile_and_run(target="verilator",
                            directory=test_dir,
                            flags=['-Wno-UNUSED', '-Wno-PINNOCONNECT'],
                            skip_compile=False,
                            skip_verilator=False)