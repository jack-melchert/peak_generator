from peak_gen.sim import arch_closure
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
            def __call__(self, a: Data, b: Data) -> Data:
                
                return a + b
            
        return Peak_Op
    return Peak_Op_fc

def test_rr():
    arch = read_arch(str(sys.argv[1]))
    PE_fc = arch_closure(arch)

    width = 16

    arch_mapper = ArchMapper(PE_fc)

    tic = time.perf_counter()
    
    ir_fc = peak_op_bw(width)
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)
    solution = ir_mapper.run_efsmt()
    
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")

    if solution is None: 
        print("No solution found for width = ", width)
        
    else:
        for i in solution.ibinding:
            print(i)

    output_binding = [((0,), ('PE_res',0))]
    rr = RewriteRule(solution.ibinding, output_binding, ir_fc, PE_fc)

    counter_example = rr.verify()

    print(counter_example)

    if counter_example is None:
        print("Passed rewrite rule verify")


    Inst_fc = inst_arch_closure(arch)
    Inst = Inst_fc(family.PyFamily())

    fields = []
    for k, v in Inst.field_dict.items():
        if issubclass(v, Tuple):
            fields.append((k, sum(1 for _ in v)))  
        else:
            fields.append((k, 0))  

    tot_length = 0
    for field, length in fields:
        if length > 0:
            for ind in range(length):
                ind_tmp = arch_mapper.input_varmap[('inst', field, ind)].size
                tot_length += ind_tmp
        else:
            ind_tmp = arch_mapper.input_varmap[('inst', field)].size
            tot_length += ind_tmp

    bin_inst = [int(i) for i in bin(solution.ibinding[0][0].value)[2:]]
    z_pad = [0 for _ in range(tot_length - len(bin_inst))]
    bin_inst = z_pad + bin_inst
    # print(bin_inst)
    bin_inst.reverse()
    

    curr_ind = 0
    for field, length in fields:
        if length > 0:
            for ind in range(length):
                ind_tmp = arch_mapper.input_varmap[('inst', field, ind)].size
                print(field)
                inst_tmp = bin_inst[curr_ind:curr_ind + ind_tmp]
                inst_tmp.reverse()
                print(inst_tmp)
                curr_ind += ind_tmp
        else:
            ind_tmp = arch_mapper.input_varmap[('inst', field)].size
            print(field)
            inst_tmp = bin_inst[curr_ind:curr_ind + ind_tmp]
            inst_tmp.reverse()
            print(inst_tmp)
            curr_ind += ind_tmp



test_rr()
