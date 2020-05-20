from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
from peak import Peak, family_closure
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
from peak_gen.asm import asm_fc
from peak_gen.config import config_arch_closure
from peak_gen.enables import enables_arch_closure
from peak_gen.alu import ALU_t, Signed_t
from peak_gen.mul import MUL_t
import json
import magma as m

import shutil 

def test_mapping_function():
    arch = read_arch(str(sys.argv[1]))
    PE_fc = arch_closure(arch)
    Inst_fc = inst_arch_closure(arch)
    Inst = Inst_fc(family.PyFamily())
    arch_mapper = ArchMapper(PE_fc)
 

    inst_type = PE_fc(family.PyFamily()).input_t.field_dict["inst"]

    _assembler = Assembler(inst_type)
    assembler = _assembler.assemble

    asm_arch_closure = asm_fc(family.PyFamily())

    gen_inst = asm_arch_closure(arch)


    with open(str(sys.argv[2])) as json_file:
        json_in = json.loads(json_file.read())
        input_binding = json_in["tuple"]
        alu = json_in["alu"]
        mul = json_in["mul"]
        mux_in0 = json_in["mux_in0"]
        mux_in1 = json_in["mux_in1"]

    print(alu)
    print(mul)
    print(mux_in0)
    print(mux_in1)
    for idx, i in enumerate(input_binding):
        if i[1][0] == "config_addr":
            i[0] = BitVector[8](int(i[0]))
        elif i[1][0] == "config_en" or i[1][0] == "enables":
            i[0] = Bit(int(i[0]))
        elif i[1][0] == "config_data":
            if "config_bit" in i[1][1]:
                i[0] = Bit(int(i[0]))
            elif i[0] == 0:
                i[0] = BitVector[16](i[0])
        elif i[1][0] == "inputs":
            if i[0][0] == 0: 
                i[0] = BitVector[16](i[0])

        if isinstance(i[0], list): 
            input_binding[idx] = tuple([(i[0][0],), tuple(i[1])])
        else:
            input_binding[idx] = tuple([i[0], tuple(i[1])])


    op_map = {}

    op_map["Mult0"] = MUL_t.Mult0
    op_map["Mult1"] = MUL_t.Mult1
    op_map["pass"] = MUL_t.Pass
    op_map["not"] = ALU_t.Sub  
    op_map["and"] = ALU_t.And    
    op_map["or"] = ALU_t.Or    
    op_map["xor"] = ALU_t.XOr    
    op_map["shl"] = ALU_t.SHL   
    op_map["lshr"] = ALU_t.SHR    
    op_map["ashr"] = ALU_t.SHR    
    op_map["neg"] = ALU_t.Sub   
    op_map["add"] = ALU_t.Add    
    op_map["sub"] = ALU_t.Sub    
    op_map["sle"] = ALU_t.LTE_Min    
    op_map["sge"] = ALU_t.GTE_Max     
    op_map["ule"] = ALU_t.LTE_Min   
    op_map["uge"] = ALU_t.GTE_Max    
    op_map["eq"] = ALU_t.Sub    
    op_map["slt"] = ALU_t.LTE_Min   
    op_map["sgt"] = ALU_t.GTE_Max  
    op_map["ult"] = ALU_t.LTE_Min    
    op_map["ugt"] = ALU_t.GTE_Max    

    alu = [op_map[n] for n in alu]
    mul = [op_map[n] for n in mul]

    mux_in0_bw = [m.math.log2_ceil(len(arch.modules[i].in0)) for i in range(len(arch.modules)) if len(arch.modules[i].in0) > 1]
    mux_in1_bw = [m.math.log2_ceil(len(arch.modules[i].in1)) for i in range(len(arch.modules)) if len(arch.modules[i].in1) > 1]

    # pdb.set_trace()

    mux_in0 = [BitVector[mux_in0_bw[i]](n) for i, n in enumerate(mux_in0)]
    mux_in1 = [BitVector[mux_in1_bw[i]](n) for i, n in enumerate(mux_in1)]

    inst_gen = gen_inst(alu=alu, mul=mul, mux_in0=mux_in0, mux_in1=mux_in1)
    input_binding.append((assembler(inst_gen), ("inst",)))

    for i in input_binding:
        print(i)



    output_binding = [((0,), ('PE_res',0))]


    shutil.copyfile(str(sys.argv[3]), "./scripts/peak_eq.py") 
    from peak_eq import mapping_function_fc

    rr = RewriteRule(input_binding, output_binding, mapping_function_fc, PE_fc)

    counter_example = rr.verify()

    print(counter_example)

    assert counter_example is None



test_mapping_function()
