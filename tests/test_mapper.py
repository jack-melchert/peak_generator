from peak_gen.sim import arch_closure
from peak_gen.arch import read_arch
import sys
from peak import Peak, family_closure, assemble
from peak.mapper import ArchMapper
from peak.mapper.utils import pretty_print_binding
import time, pytest

@family_closure
def Add_fc(family):
    Data = family.BitVector[16]
    Data32 = family.BitVector[32]
    @assemble(family, locals(), globals())
    class Add(Peak):
        def __call__(self, a:Data, b:Data) -> Data:
            return a + b
    return Add

@family_closure
def Add4_fc(family):
    Data = family.BitVector[4]
    @assemble(family, locals(), globals())
    class Add4(Peak):
        def __call__(self, a:Data, b:Data) -> Data:
            return a + b
    return Add4

@family_closure
def Mul_Add_fc(family):
    Data = family.BitVector[16]
    Data32 = family.BitVector[32]
    @assemble(family, locals(), globals())
    class Mul_Add(Peak):
        def __call__(self, a:Data, b:Data, c:Data) -> Data:
            return a * b + c
    return Mul_Add


@pytest.mark.parametrize("arch_file", ["examples/mapper_tests/test_alu4_alu4.json"])
def test_4_bit_add(arch_file):
    arch = read_arch(str(arch_file))
    PE_fc = arch_closure(arch)

    ir_fc = Add4_fc

    tic = time.perf_counter()

    arch_mapper = ArchMapper(PE_fc)
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)
    solution = ir_mapper.solve('cvc4')
    pretty_print_binding(solution.ibinding)
    assert solution.solved

    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")

@pytest.mark.parametrize("arch_file", ["examples/misc_tests/test_add.json"])
def test_no_mapping(arch_file):
    arch = read_arch(str(arch_file))
    PE_fc = arch_closure(arch)

    ir_fc = Mul_Add_fc

    tic = time.perf_counter()

    arch_mapper = ArchMapper(PE_fc)
    ir_mapper = arch_mapper.process_ir_instruction(ir_fc)
    solution = ir_mapper.solve('cvc4')
    assert not solution.solved

    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")

@pytest.mark.parametrize("arch_file", ["examples/misc_tests/test_add.json", "examples/misc_tests/test_alu.json", "examples/mapper_tests/test_add_alu.json", "examples/mapper_tests/test_mul_alu.json", "examples/mapper_tests/test_mul_add.json"])
def test_add_all_files(arch_file):
    arch = read_arch(str(arch_file))
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


# Really long
@pytest.mark.skip
@pytest.mark.parametrize("arch_file", ["examples/mapper_tests/test_alu_alu.json"])
def test_alu_alu(arch_file):
    arch = read_arch(str(arch_file))
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