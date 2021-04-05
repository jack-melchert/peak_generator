from peak_gen.sim import fp_pe_arch_closure, pe_arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
from peak_gen.peak_wrapper import wrapped_peak_class
from peak import Peak, family_closure, Const
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
from hwtypes import BitVector, Tuple, Bit
import sys
from peak import family
from peak.family import AbstractFamily
from peak.mapper import RewriteRule
from peak.assembler.assembled_adt import  AssembledADT
from peak.assembler.assembler import Assembler
import pdb
import json
import copy 
from pysmt.logics import QF_BV
import time
# from lassen.sim import PE_fc
# from metamapper.irs.coreir.ir import gen_peak_CoreIR

def peak_op_bw():
    @family_closure
    def Peak_Op_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        SData = family.Signed[16]
        Bit = family.Bit
        # @family.assemble(locals(), globals())
        class Peak_Op(Peak):

            def __call__(self, data176 : Data, data177 : Data, data178 : Data, data179 : Data, data180 : Data, data181 : Data, data182 : Data) -> Data:
                return Data(Data(data177 * data178) + Data(Data(data179 * data180) + Data(Data(data181 * data182) + data176)))
            # def __call__(self, data176 : Data, data177 : Data) -> Data:
            #     return data177 + data176
        return Peak_Op
    return Peak_Op_fc

def test_rr():
    arch = read_arch(str(sys.argv[1]))
    # PE_fc = pe_arch_closure(arch)
    PE_fc = wrapped_peak_class(arch, debug=True)

    constraints = {("inputs0",): ('data176',), ("inputs1",): ('data177',), ("inputs2",): ('data178',), ("inputs3",): ('data179',), ("inputs4",): ('data180',), ("inputs5",): ('data181',), ("inputs6",): ('data182',)}


    arch_mapper = ArchMapper(PE_fc, input_constraints=constraints)
    # arch_mapper = ArchMapper(PE_fc)
    ir_fc = peak_op_bw()
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)

    start = time.time()
    solution = ir_mapper.solve('z3')
    end = time.time()

    print("time elapsed:", end-start)

    if solution is None: 
        print("No solution found")
    else:
        print("Solution found!")
        # print(solution.ibinding)
        # pretty_print_binding(solution.obinding) 
    #     counter_example = solution.verify()

    #     if counter_example is None:
    #         print("Passed verification")
    #     else:
    #         print("Failed verification")
    #         print(counter_example)

test_rr()
