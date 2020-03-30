from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch
import sys
from peak import Peak, family_closure, assemble
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
import time

@family_closure
def Add_fc(family):
    Data = family.BitVector[16]
    Data32 = family.BitVector[32]
    @assemble(family, locals(), globals())
    class Add(Peak):
        def __call__(self, a:Data, b:Data) -> Data:
            return a + b
    return Add

def test_add():
    arch = read_arch(str(sys.argv[1]))
    PE_fc = arch_closure(arch)

    ir_fc = Add_fc

    tic = time.perf_counter()

    arch_mapper = ArchMapper(PE_fc)
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)
    solution = ir_mapper.solve('cvc4')
    pretty_print_binding(solution.ibinding)
    assert solution.solved

    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")

test_add()
