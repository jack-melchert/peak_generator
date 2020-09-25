from peak_gen.sim import pe_arch_closure
from peak_gen.arch import read_arch
import sys
from peak import Peak, family_closure
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
import time, pytest
from peak import family
from peak.family import AbstractFamily

@family_closure
def Add_fc(family : AbstractFamily):
    Data = family.BitVector[16]
    Data32 = family.BitVector[32]
    @family.assemble(locals(), globals())
    class Add(Peak):
        def __call__(self, a:Data, b:Data) -> Data:
            return a + b
    return Add

@family_closure
def Add_4_ins_fc(family : AbstractFamily):
    Data = family.BitVector[16]
    Data32 = family.BitVector[32]
    @family.assemble(locals(), globals())
    class Add_4_ins(Peak):
        def __call__(self, a:Data, b:Data, c:Data, d:Data) -> Data:
            return a + b + c + d
    return Add_4_ins

@family_closure
def Add_4_bit_fc(family : AbstractFamily):
    Data = family.BitVector[4]
    @family.assemble(locals(), globals())
    class Add_4_bit(Peak):
        def __call__(self, a:Data, b:Data, c:Data) -> Data:
            return a + b + c
    return Add_4_bit

@family_closure
def Mul_Add_fc(family : AbstractFamily):
    Data = family.BitVector[16]
    Data32 = family.BitVector[32]
    @family.assemble(locals(), globals())
    class Mul_Add(Peak):
        def __call__(self, a:Data, b:Data, c:Data) -> Data:
            return a * b + c
    return Mul_Add



@pytest.mark.parametrize("arch_file", ["examples/misc_tests/test_add.json"])
def test_no_mapping(arch_file):
    arch = read_arch(str(arch_file))
    PE_fc = pe_arch_closure(arch)

    ir_fc = Mul_Add_fc

    tic = time.perf_counter()

    arch_mapper = ArchMapper(PE_fc)
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)
    solution = ir_mapper.solve('z3')
    assert solution is None

    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")

@pytest.mark.parametrize("arch_file", ["examples/misc_tests/test_add.json", "examples/misc_tests/test_alu.json"])
def test_add_all_files(arch_file):
    arch = read_arch(str(arch_file))
    PE_fc = pe_arch_closure(arch)

    ir_fc = Add_fc

    tic = time.perf_counter()

    arch_mapper = ArchMapper(PE_fc)
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)
    solution = ir_mapper.solve('z3')
    pretty_print_binding(solution.ibinding)
    assert solution is not None

    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")



@pytest.mark.parametrize("arch_file", ["examples/mapper_tests/test_alu_alu_alu.json"])
def test_efsmt(arch_file):
    arch = read_arch(str(arch_file))
    PE_fc = pe_arch_closure(arch)

    ir_fc = Add_4_ins_fc

    tic = time.perf_counter()

    arch_mapper = ArchMapper(PE_fc)
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)
    solution = ir_mapper.solve(external_loop=True)
    pretty_print_binding(solution.ibinding)

    assert solution is not None

    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")