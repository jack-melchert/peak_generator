from peak_gen.sim import pe_arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
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
        Bit = family.Bit
        @family.assemble(locals(), globals())
        class Peak_Op(Peak):
            def __call__(self, a:Data) -> Data:
                return a
            
        return Peak_Op
    return Peak_Op_fc

def test_rr():
    arch = read_arch(str(sys.argv[1]))
    PE_fc = pe_arch_closure(arch)

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
        for i in solution.ibinding:
            print(i)
        for i in solution.obinding:
            print(i)
        counter_example = solution.verify()
        print(counter_example)



    # input_binding = [(BitVector[1](0), ('inst', 'mul', 0)), (BitVector[4](0), ('inst', 'alu', 0)), (BitVector[5](0), ('inst', 'cond', 0)),  (BitVector[1](0), ('inst', 'signed')), (BitVector[8](0), ('inst', 'lut')), 
    # (('a',), ('inputs', 0)), (('b',), ('inputs', 1)), (BitVector[16](0), ('inputs', 2)), 
    # (Bit(1), ('bit_inputs', 0)), (Bit(1), ('bit_inputs', 1)), (Bit(1), ('bit_inputs', 2)), (Bit(1), ('clk_en',))]
    
    # output_binding = [((0,), ('pe_outputs', 0))]

    # rr = RewriteRule(input_binding, output_binding, ir_fc, PE_fc)

    # counter_example = rr.verify()
    # print(counter_example)

    # if counter_example is None:
    #     print("Passed rewrite rule verify")


test_rr()
