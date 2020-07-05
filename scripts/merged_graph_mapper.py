from peak_gen.sim import wrapped_pe_arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
from peak import Peak, family_closure
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
import hwtypes 
from hwtypes import BitVector, Tuple, Bit, bit_vector
import sys
import time
import peak
from peak import family
from peak.family import AbstractFamily
from peak.mapper import RewriteRule
from peak.assembler.assembled_adt import  AssembledADT
from peak.assembler.assembler import Assembler

import json
import jsonpickle
import magma as m

import shutil 

def test_verify_rr():
    arch = read_arch(str(sys.argv[1]))
    PE_fc = wrapped_pe_arch_closure(arch)

    with open(str(sys.argv[2])) as json_file:
        rewrite_rule_in = jsonpickle.decode(json_file.read())

    input_binding = []

    input_binding_tmp = rewrite_rule_in["ibinding"]

    for i in input_binding_tmp:
        
        if isinstance(i[0], dict):
            u = i[0]
            v = i[1]
            if u['type'] == "BitVector":
                u = (BitVector[u['width']](u['value']))
            elif u['type'] == "Bit":
                u = (Bit(u['value']))

            input_binding.append(tuple([u, tuple(v) ])) 
        elif i[0] == "unbound":
            input_binding.append(tuple( [peak.mapper.utils.Unbound, tuple(i[1])] ))
        else:
            input_binding.append(tuple( [tuple(i[0]), tuple(i[1])] ))
        
    for i in input_binding:
        print(i)

    output_binding_tmp = rewrite_rule_in["obinding"]
    output_binding = []

    for o in output_binding_tmp:
        output_binding.append(tuple( [tuple(o[0]), tuple(o[1])] ))

    shutil.copyfile(str(sys.argv[3]), "./scripts/peak_eq.py") 
    from peak_eq import mapping_function_fc

    rr = RewriteRule(input_binding, output_binding, mapping_function_fc, PE_fc)

    counter_example = rr.verify()

    if counter_example is None:
        print("Passed rewrite rule verify")
    else:
        print("Failed rewrite rule verify")
        print(counter_example)

test_verify_rr()

