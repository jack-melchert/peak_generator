from collections import namedtuple
import operator
import peak_gen.asm as asm
from peak_gen.sim import pe_arch_closure
from peak_gen.arch import read_arch
from hwtypes import SIntVector, UIntVector, BitVector, Bit, Tuple
import pytest
import random
from peak import family

arch = read_arch(str("examples/misc_tests/test_lut.json"))
PE_fc = pe_arch_closure(arch)
PE = PE_fc(family.PyFamily())
Data = BitVector[arch.input_width]
DataInputList = Tuple[(Data for _ in range(arch.num_inputs))]
BitInputList = Tuple[(Bit for _ in range(arch.num_bit_inputs + 3))]

op = namedtuple("op", ["name", "func"])
NTESTS = 32

@pytest.mark.parametrize("op", [
    op('and', lambda x, y: x&y),
    op('or',  lambda x, y: x|y),
    op('xor',  lambda x, y: x^y),
])
def test_lut_binary(op):
    pe = PE()
    inst = getattr(asm, f"lut_{op.name}")(arch)
    for _ in range(NTESTS):
        config_data_bits = BitVector.random(3)
        b0 = config_data_bits[0]
        b1 = config_data_bits[1]
        b2 = config_data_bits[2]
        input_data = [UIntVector.random(arch.input_width) for _ in range(arch.num_inputs)]
        input_data += [b0, b1, b2]
        _, res_p  = pe(inst = inst, inputs = DataInputList(*input_data))
        assert res_p==op.func(b1,b2) #Testing from bit1 and bit2 port

@pytest.mark.parametrize("op", [
    op('not', lambda x: ~x),
])
def test_lut_unary(op):
    pe = PE()
    inst = getattr(asm, f"lut_{op.name}")(arch)
    for _ in range(NTESTS):
        config_data_bits = BitVector.random(3)
        b0 = config_data_bits[0]
        b1 = config_data_bits[1]
        b2 = config_data_bits[2]
        input_data = [UIntVector.random(arch.input_width) for _ in range(arch.num_inputs)]
        input_data += [b0, b1, b2]
        _, res_p  = pe(inst = inst, inputs = DataInputList(*input_data))
        assert res_p==op.func(b1)

@pytest.mark.parametrize("op", [
    op('mux', lambda sel, d0, d1: d1 if sel else d0),
])
def test_lut_ternary(op):
    pe = PE()
    inst = getattr(asm, f"lut_{op.name}")(arch)
    for _ in range(NTESTS):

        config_data_bits = BitVector.random(3)
        sel = config_data_bits[2]
        d0 = config_data_bits[0]
        d1 = config_data_bits[1]

        input_data = [UIntVector.random(arch.input_width) for _ in range(arch.num_inputs)]

        input_data += [b0, b1, b2]
        _, res_p  = pe(inst = inst, inputs = DataInputList(*input_data))
        assert res_p==op.func(sel,d0,d1)

def test_lut():
    pe = PE()
    for _ in range(NTESTS):
        lut_val = BitVector.random(8)
        inst = asm.lut(arch, lut_val)

        config_data_bits = BitVector.random(3)
        b0 = config_data_bits[0]
        b1 = config_data_bits[1]
        b2 = config_data_bits[2]
        input_data = [UIntVector.random(arch.input_width) for _ in range(arch.num_inputs)]
        input_data += [b0, b1, b2]
        _, res_p  = pe(inst = inst, inputs = DataInputList(*input_data))
        assert res_p== lut_val[int(BitVector[3]([b0,b1,b2]))]

# test_lut()