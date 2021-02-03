from peak_gen.sim import fp_pe_arch_closure, pe_arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
from peak_gen.peak_wrapper import wrapped_peak_class
from peak import Peak, family_closure, Const
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
from hwtypes import BitVector, Tuple, Bit
import sys
from timeit import default_timer as timer
from peak import family
from peak.family import AbstractFamily
from peak.mapper import RewriteRule
from peak.assembler.assembled_adt import  AssembledADT
from peak.assembler.assembler import Assembler
import pdb
import json
import copy 
from pysmt.logics import QF_BV
# from lassen.sim import PE_fc
# from metamapper.irs.coreir.ir import gen_peak_CoreIR

def peak_op_bw():
    @family_closure
    def Peak_Op_fc(family: AbstractFamily):
        Data = family.BitVector[16]
        SData = family.Signed[16]
        Bit = family.Bit
        @family.assemble(locals(), globals())
        class Peak_Op(Peak):

            def __call__(self, in1 : Bit, in0 : Bit, in2 : Bit) -> Bit:
                
                return in0 & in1 & in2
            
        return Peak_Op
    return Peak_Op_fc

def test_rr():
    arch = read_arch(str(sys.argv[1]))
    # PE_fc = pe_arch_closure(arch)
    PE_fc = wrapped_peak_class(arch)


    arch_mapper = ArchMapper(PE_fc)


    ir_fc = peak_op_bw()
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)


    solution = ir_mapper.solve()


    if solution is None: 
        print("No solution found")
    else:
        # pretty_print_binding(solution.ibinding)
        # pretty_print_binding(solution.obinding) 
        counter_example = solution.verify()

        if counter_example is None:
            print("Passed verification")
        else:
            print("Failed verification")
            print(counter_example)

test_rr()
