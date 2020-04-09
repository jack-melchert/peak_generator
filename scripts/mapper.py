from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch
from peak_gen.isa import inst_arch_closure
from peak import Peak, family_closure, assemble
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
from hwtypes import BitVector, Tuple
import sys
import time

@family_closure
def Add_fc(family):
    Data = family.BitVector[16]
    Bit = family.Bit
    @assemble(family, locals(), globals())
    class Add(Peak):
        def __call__(self, a:Data, b:Data) -> Data:

            return a + b
          
    return Add

def test_add():
    arch = read_arch(str(sys.argv[1]))
    PE_fc = arch_closure(arch)
    Inst_fc = inst_arch_closure(arch)
    Inst = Inst_fc(BitVector.get_family())
    ALU_t = Inst.alu[0]

    ir_fc = Add_fc

    tic = time.perf_counter()

    inst_restrict = int('10000000000', 2)
    print(inst_restrict)
    arch_mapper = ArchMapper(PE_fc)
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)
    solution = ir_mapper.solve('cvc4')
    pretty_print_binding(solution.ibinding)
    # import pdb; pdb.set_trace()
    assert solution.solved

    # print(hex(solution.ibinding[0][0].value))



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


    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")

test_add()
