from peak_gen.sim import fp_pe_arch_closure, pe_arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
from peak_gen.peak_wrapper import wrapped_peak_class
from peak import Peak, family_closure, Const
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
from hwtypes import BitVector, Tuple, Bit
import sys
import time
from peak import family
from peak.family import AbstractFamily
from peak.mapper import RewriteRule
from peak.assembler.assembled_adt import  AssembledADT
from peak.assembler.assembler import Assembler
import pdb
import json
import copy 


def peak_op_bw(width):
    @family_closure
    def Peak_Op_fc(family: AbstractFamily):
        Data = family.BitVector[width]
        SData = family.Signed[width]
        Bit = family.Bit
        @family.assemble(locals(), globals())
        class Peak_Op(Peak):

            def __call__(self, in0 : Data, in1 : Data) -> Data:
                
                return in0 + in1
            
        return Peak_Op
    return Peak_Op_fc

def test_rr():
    arch = read_arch(str(sys.argv[1]))
    # PE_fc = pe_arch_closure(arch)
    PE_fc = wrapped_peak_class(arch)

    width = 16

    arch_mapper = ArchMapper(PE_fc)

    tic = time.perf_counter()
    
    ir_fc = peak_op_bw(width)
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)
    solution = ir_mapper.solve('z3', external_loop=True)
    
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")

    if solution is None: 
        print("No solution found for width = ", width)
    else:
        pretty_print_binding(solution.ibinding)
        pretty_print_binding(solution.obinding) 
        counter_example = solution.verify()

        if counter_example is None:
            print("Passed verification")
        else:
            print("Failed verification")
            print(counter_example)

test_rr()
