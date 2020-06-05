from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
from peak import Peak, family_closure
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
import hwtypes 
from hwtypes import BitVector, Tuple, Bit, bit_vector
import sys
import time
from peak import family
from peak.family import AbstractFamily
from peak.mapper import RewriteRule
from peak.assembler.assembled_adt import  AssembledADT
from peak.assembler.assembler import Assembler
from peak_gen.asm import asm_fc
from peak_gen.config import config_arch_closure
from peak_gen.enables import enables_arch_closure
from peak_gen.alu import ALU_t, Signed_t
from peak_gen.mul import MUL_t
import json
import jsonpickle
import magma as m

import shutil 

def test_verify_rr():
    arch = read_arch(str(sys.argv[1]))
    PE_fc = arch_closure(arch)

    with open(str(sys.argv[2])) as json_file:
        input_binding_tmp = jsonpickle.decode(json_file.read())

    input_binding = []

    for i in input_binding_tmp:
        
        if isinstance(i[0], dict):
            u = i[0]
            v = i[1]
            if u['type'] == "BitVector":
                u = (BitVector[u['width']](u['value']))
            elif u['type'] == "Bit":
                u = (Bit(u['value']))

            input_binding.append(tuple([u, tuple(v) ])) 
        else:
            input_binding.append(tuple( [tuple(i[0]), tuple(i[1])] ))
        
    for i in input_binding:
        print(i)

    output_binding = [((0,), ('PE_res',0))]

    shutil.copyfile(str(sys.argv[3]), "./scripts/peak_eq.py") 
    from peak_eq import mapping_function_fc

    rr = RewriteRule(input_binding, output_binding, mapping_function_fc, PE_fc)

    counter_example = rr.verify()


    if counter_example is None:
        print("Passed rewrite rule verify")
    else:
        print("Failed rewrite rule verify")
        print(counter_example)


def test_gen_rr():
    print()
    print("Starting rewrite rule generation")

    arch = read_arch(str(sys.argv[1]))
    PE_fc = arch_closure(arch)

    arch_mapper = ArchMapper(PE_fc)
    

    from peak_eq import mapping_function_fc

    ir_mapper = arch_mapper.process_ir_instruction(mapping_function_fc)
    solution = ir_mapper.run_efsmt()

    if solution is None: 
        print("No solution found for width = ", width)
        
    else:
        for i in solution.ibinding:
            print(i)

test_verify_rr()
# test_gen_rr()
