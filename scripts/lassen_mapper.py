
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
import time
from lassen.sim import PE_fc
# from metamapper.irs.coreir.ir import gen_peak_CoreIR

def peak_op_bw():
    @family_closure
    def Peak_Op_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        SData = family.Signed[16]
        Bit = family.Bit
        # @family.assemble(locals(), globals())
        class Peak_Op(Peak):

            def __call__(self, in_0 : Data, in_1 : Data) -> Data:
                # return Bit(SData(in_0) <= SData(in_1 + 1))
                return in_0 + in_1 * 3
        return Peak_Op
    return Peak_Op_fc

def test_rr():

    arch_mapper = ArchMapper(PE_fc)

    ir_fc = peak_op_bw()
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)

    start = time.time()
    solution = ir_mapper.solve('z3', write_file=f"smtlib/test.smt2")
    end = time.time()

    print("time elapsed:", end-start)

    if solution is None: 
        print("No solution found")
    else:
        print("Solution found!")
    #     # pretty_print_binding(solution.ibinding)
    #     # pretty_print_binding(solution.obinding) 
    #     counter_example = solution.verify()

    #     if counter_example is None:
    #         print("Passed verification")
    #     else:
    #         print("Failed verification")
    #         print(counter_example)

test_rr()
